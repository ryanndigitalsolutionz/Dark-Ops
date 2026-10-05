import hashlib
import json
import os
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from flask import current_app

from extensions import db
from models.alert import Alert
from models.application import Application
from models.asset import Asset
from models.event import Event


WEB_TYPES = {"web", "website", "web_app", "web_application"}
ANDROID_TYPES = {"android", "android_app", "mobile", "mobile_app"}
WINDOWS_TYPES = {"windows", "windows_app", "desktop", "desktop_app"}

SEVERITY_ORDER = {
    "informational": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

DETECTION_CATALOGUE = {
    "availability": {
        "category": "availability",
        "mode": "passive",
        "platforms": ["web", "android", "windows"],
    },
    "tls_certificate": {
        "category": "transport",
        "mode": "passive",
        "platforms": ["web"],
    },
    "security_headers": {
        "category": "configuration",
        "mode": "passive",
        "platforms": ["web"],
    },
    "cors": {
        "category": "access_control",
        "mode": "passive",
        "platforms": ["web"],
    },
    "cookies": {
        "category": "configuration",
        "mode": "passive",
        "platforms": ["web"],
    },
    "error_exposure": {
        "category": "configuration",
        "mode": "passive",
        "platforms": ["web"],
    },
    "server_disclosure": {
        "category": "configuration",
        "mode": "passive",
        "platforms": ["web"],
    },
    "dangerous_methods": {
        "category": "access_control",
        "mode": "passive",
        "platforms": ["web"],
    },
    "dns_change": {
        "category": "integrity",
        "mode": "passive",
        "platforms": ["web"],
    },
    "ip_change": {
        "category": "integrity",
        "mode": "passive",
        "platforms": ["web"],
    },
    "redirect_change": {
        "category": "transport",
        "mode": "passive",
        "platforms": ["web"],
    },
    "a01_protected_route": {
        "category": "access_control",
        "mode": "authorized_active",
        "platforms": ["web"],
    },
    "client_observation": {
        "category": "device",
        "mode": "client_telemetry",
        "platforms": ["android", "windows"],
    },
    "asset_finding": {
        "category": "asset_context",
        "mode": "document_derived",
        "platforms": ["web", "android", "windows"],
    },
}


class DetectionError(Exception):
    pass


def utcnow():
    return datetime.now(timezone.utc)


def _timeout():
    return int(current_app.config.get(
        "DARKOPS_DETECTION_TIMEOUT_SECONDS",
        10,
    ))


def _user_agent():
    return current_app.config.get(
        "DARKOPS_DETECTION_USER_AGENT",
        "DarkOps/1.0",
    )


def _fingerprint(value):
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")

    return hashlib.sha256(encoded).hexdigest()


def _application_state(application):
    state = getattr(application, "detection_state", None)

    if not isinstance(state, dict):
        state = {}

    return state


def _set_state(application, state):
    application.detection_state = state


def _get_url_pair(application):
    urls = []

    if application.authorized_primary_url:
        urls.append(("frontend", application.authorized_primary_url))

    if application.base_url:
        urls.append(("backend", application.base_url))

    return urls


def _validate_https(url):
    parsed = urllib.parse.urlparse(url)

    if parsed.scheme.lower() != "https":
        raise DetectionError(
            "DarkOps only protects HTTPS web application URLs."
        )

    if not parsed.hostname:
        raise DetectionError("Application URL has no valid hostname.")

    return parsed


def _fetch(url, method="GET", headers=None):
    request_headers = {
        "User-Agent": _user_agent(),
        "Accept": "*/*",
    }

    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(
        url,
        headers=request_headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=_timeout(),
        ) as response:
            body = response.read(65536)

            return {
                "status": response.status,
                "headers": dict(response.headers.items()),
                "final_url": response.geturl(),
                "body": body.decode("utf-8", errors="replace"),
            }

    except urllib.error.HTTPError as error:
        body = error.read(65536)

        return {
            "status": error.code,
            "headers": dict(error.headers.items()),
            "final_url": error.geturl(),
            "body": body.decode("utf-8", errors="replace"),
        }


def _certificate_details(hostname, port=443):
    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, port),
        timeout=_timeout(),
    ) as raw_socket:
        with context.wrap_socket(
            raw_socket,
            server_hostname=hostname,
        ) as tls_socket:
            certificate = tls_socket.getpeercert()

            ssl.match_hostname(
                certificate,
                hostname,
            )

            return {
                "subject": certificate.get("subject"),
                "issuer": certificate.get("issuer"),
                "serial_number": certificate.get("serialNumber"),
                "not_before": certificate.get("notBefore"),
                "not_after": certificate.get("notAfter"),
                "tls_version": tls_socket.version(),
            }


def _resolve_ips(hostname):
    results = socket.getaddrinfo(
        hostname,
        443,
        type=socket.SOCK_STREAM,
    )

    return sorted({
        result[4][0]
        for result in results
        if result[4]
    })


def _ip_enrichment(ip):
    token = current_app.config.get(
        "IPINFO_TOKEN"
    ) or os.getenv("IPINFO_TOKEN")

    url = f"https://ipinfo.io/{urllib.parse.quote(ip, safe='')}/json"

    if token:
        url = f"{url}?token={urllib.parse.quote(token, safe='')}"

    try:
        result = _fetch(url)

        if result["status"] >= 400:
            return None

        data = json.loads(result["body"])

        privacy = data.get("privacy") or {}

        country = data.get("country")

        country_context = _country_enrichment(country)

        return {
            "ip": data.get("ip", ip),
            "hostname": data.get("hostname"),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": country,
            "loc": data.get("loc"),
            "org": data.get("org"),
            "asn": data.get("asn"),
            "vpn": privacy.get("vpn"),
            "proxy": privacy.get("proxy"),
            "tor": privacy.get("tor"),
            "relay": privacy.get("relay"),
            "country_context": country_context,
        }

    except (urllib.error.URLError, ValueError, json.JSONDecodeError):
        return None


def _country_enrichment(country_code):
    if not country_code:
        return None

    token = current_app.config.get(
        "REST_COUNTRIES_API_KEY"
    ) or os.getenv("REST_COUNTRIES_API_KEY")

    if not token:
        return None

    url = (
        "https://api.restcountries.com/countries/v5/"
        f"codes.alpha_2/{urllib.parse.quote(country_code, safe='')}"
    )

    try:
        result = _fetch(
            url,
            headers={"Authorization": f"Bearer {token}"},
        )

        if result["status"] >= 400:
            return None

        payload = json.loads(result["body"])
        objects = payload.get("data", {}).get("objects", [])

        if not objects:
            return None

        country = objects[0]

        return {
            "name": (country.get("names") or {}).get("common"),
            "alpha_2": (country.get("codes") or {}).get("alpha_2"),
            "alpha_3": (country.get("codes") or {}).get("alpha_3"),
            "region": country.get("region"),
            "subregion": country.get("subregion"),
        }

    except (urllib.error.URLError, ValueError, json.JSONDecodeError):
        return None


def _observation(
    check_id,
    source,
    event_type,
    severity,
    title,
    description,
    evidence=None,
    security_relevant=False,
    alert=False,
    retain_on_first=True,
    alert_on_first=False,
    mode=None,
    asset_id=None,
):
    return {
        "check_id": check_id,
        "source": source,
        "event_type": event_type,
        "severity": severity,
        "title": title,
        "description": description,
        "evidence": evidence or {},
        "security_relevant": security_relevant,
        "alert": alert,
        "retain_on_first": retain_on_first,
        "alert_on_first": alert_on_first,
        "mode": mode or DETECTION_CATALOGUE.get(
            check_id,
            {},
        ).get("mode", "passive"),
        "category": DETECTION_CATALOGUE.get(
            check_id,
            {},
        ).get("category", "security"),
        "asset_id": asset_id,
    }


def inspect_web_endpoint(application, label, url):
    parsed = _validate_https(url)
    observations = []

    try:
        response = _fetch(url)
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        observations.append(
            _observation(
                "availability",
                "web",
                "availability_failure",
                "high",
                f"{label.title()} is unreachable",
                f"DarkOps could not reach the {label} deployment.",
                {"url": url, "error": str(error)},
                security_relevant=True,
                alert=True,
                alert_on_first=True,
            )
        )
        return observations

    status = response["status"]

    observations.append(
        _observation(
            "availability",
            "web",
            "availability_state",
            "informational",
            f"{label.title()} availability checked",
            f"{label.title()} responded to the protection cycle.",
            {
                "url": url,
                "status": status,
            },
            security_relevant=False,
        )
    )

    final_url = response["final_url"]

    if not final_url.lower().startswith("https://"):
        observations.append(
            _observation(
                "redirect_change",
                "web",
                "https_redirect_downgrade",
                "high",
                f"{label.title()} redirects away from HTTPS",
                "The protected deployment redirects to a non-HTTPS destination.",
                {
                    "url": url,
                    "final_url": final_url,
                },
                security_relevant=True,
                alert=True,
                alert_on_first=True,
            )
        )

    headers = {
        key.lower(): value
        for key, value in response["headers"].items()
    }

    required_headers = {
        "strict-transport-security": "HSTS",
        "content-security-policy": "CSP",
        "x-content-type-options": "X-Content-Type-Options",
        "referrer-policy": "Referrer-Policy",
        "permissions-policy": "Permissions-Policy",
    }

    missing_headers = [
        label_name
        for header, label_name in required_headers.items()
        if header not in headers
    ]

    observations.append(
        _observation(
            "security_headers",
            "web",
            "security_header_state",
            "low",
            f"{label.title()} security headers checked",
            "DarkOps compared the deployment's observable security headers.",
            {
                "url": url,
                "missing": missing_headers,
                "present": [
                    value
                    for key, value in required_headers.items()
                    if key in headers
                ],
            },
            security_relevant=bool(missing_headers),
            alert=bool(missing_headers),
            alert_on_first=False,
        )
    )

    allow_origin = headers.get("access-control-allow-origin")
    allow_credentials = headers.get("access-control-allow-credentials")

    cors_problem = (
        allow_origin == "*"
        and str(allow_credentials).lower() == "true"
    )

    observations.append(
        _observation(
            "cors",
            "web",
            "cors_security_state",
            "high" if cors_problem else "informational",
            f"{label.title()} CORS policy checked",
            "DarkOps checked the observable CORS response policy.",
            {
                "allow_origin": allow_origin,
                "allow_credentials": allow_credentials,
                "wildcard_with_credentials": cors_problem,
            },
            security_relevant=cors_problem,
            alert=cors_problem,
            alert_on_first=True,
        )
    )

    set_cookie = response["headers"].get_all("Set-Cookie") \
        if hasattr(response["headers"], "get_all") else []

    cookie_findings = []

    for cookie in set_cookie:
        lowered = cookie.lower()
        cookie_findings.append({
            "secure": "secure" in lowered,
            "httponly": "httponly" in lowered,
            "samesite": "samesite=" in lowered,
        })

    insecure_cookies = [
        finding for finding in cookie_findings
        if not (
            finding["secure"]
            and finding["httponly"]
            and finding["samesite"]
        )
    ]

    observations.append(
        _observation(
            "cookies",
            "web",
            "cookie_security_state",
            "medium" if insecure_cookies else "informational",
            f"{label.title()} cookie security checked",
            "DarkOps inspected observable cookie security attributes.",
            {
                "cookies_checked": len(cookie_findings),
                "findings": cookie_findings,
            },
            security_relevant=bool(insecure_cookies),
            alert=bool(insecure_cookies),
            alert_on_first=True,
        )
    )

    body_lower = response["body"].lower()

    error_markers = [
        "traceback",
        "stack trace",
        "syntaxerror",
        "sqlalchemy.exc",
        "django.core.exceptions",
        "flask debug",
        "exception in thread",
        "fatal error",
    ]

    exposed_errors = [
        marker for marker in error_markers
        if marker in body_lower
    ]

    observations.append(
        _observation(
            "error_exposure",
            "web",
            "error_information_exposure",
            "high" if exposed_errors else "informational",
            f"{label.title()} error exposure checked",
            "DarkOps checked the response for observable debugging or stack-trace information.",
            {
                "markers": exposed_errors,
                "status": status,
            },
            security_relevant=bool(exposed_errors),
            alert=bool(exposed_errors),
            alert_on_first=True,
        )
    )

    server = headers.get("server")
    x_powered_by = headers.get("x-powered-by")

    disclosure = {
        "server": server,
        "x_powered_by": x_powered_by,
    }

    observations.append(
        _observation(
            "server_disclosure",
            "web",
            "server_information_disclosure",
            "low" if server or x_powered_by else "informational",
            f"{label.title()} server disclosure checked",
            "DarkOps checked whether response headers expose server implementation information.",
            disclosure,
            security_relevant=bool(server or x_powered_by),
            alert=False,
        )
    )

    try:
        allow = _fetch(
            url,
            method="OPTIONS",
        )["headers"].get("Allow", "")

        dangerous_methods = [
            method for method in ("TRACE",)
            if method in {
                item.strip().upper()
                for item in allow.split(",")
            }
        ]

        observations.append(
            _observation(
                "dangerous_methods",
                "web",
                "dangerous_http_method_exposure",
                "medium" if dangerous_methods else "informational",
                f"{label.title()} HTTP methods checked",
                "DarkOps inspected the server's advertised HTTP methods.",
                {
                    "allow": allow,
                    "dangerous_methods": dangerous_methods,
                },
                security_relevant=bool(dangerous_methods),
                alert=bool(dangerous_methods),
                alert_on_first=True,
            )
        )
    except (urllib.error.URLError, OSError):
        pass

    hostname = parsed.hostname

    try:
        ips = _resolve_ips(hostname)
    except OSError:
        ips = []

    current_dns = {
        "hostname": hostname,
        "ips": ips,
    }

    ip_context = [
        context for ip in ips
        if (context := _ip_enrichment(ip))
    ]

    current_dns["ip_context"] = ip_context

    observations.append(
        _observation(
            "dns_change",
            "web",
            "dns_state",
            "medium",
            f"{label.title()} DNS state checked",
            "DarkOps observed the current public DNS resolution.",
            current_dns,
            security_relevant=True,
            alert=True,
            retain_on_first=False,
            alert_on_first=False,
        )
    )

    observations.append(
        _observation(
            "ip_change",
            "ipinfo",
            "infrastructure_ip_state",
            "medium",
            f"{label.title()} infrastructure IP state checked",
            "DarkOps enriched the deployment's observed public IP context.",
            {
                "hostname": hostname,
                "ips": ips,
                "ip_context": ip_context,
            },
            security_relevant=True,
            alert=True,
            retain_on_first=False,
            alert_on_first=False,
        )
    )

    try:
        certificate = _certificate_details(hostname)

        observations.append(
            _observation(
                "tls_certificate",
                "tls",
                "tls_certificate_state",
                "informational",
                f"{label.title()} TLS certificate checked",
                "DarkOps verified the observable TLS certificate and hostname.",
                certificate,
                security_relevant=False,
            )
        )

    except Exception as error:
        observations.append(
            _observation(
                "tls_certificate",
                "tls",
                "tls_certificate_failure",
                "high",
                f"{label.title()} TLS validation failed",
                "DarkOps could not validate the deployment's TLS certificate.",
                {
                    "hostname": hostname,
                    "error": str(error),
                },
                security_relevant=True,
                alert=True,
                alert_on_first=True,
            )
        )

    return observations


def inspect_protected_routes(
    application,
    routes,
):
    observations = []

    for route in routes or []:
        if not isinstance(route, dict):
            continue

        path = route.get("path")

        if not path:
            continue

        base_url = application.base_url or application.authorized_primary_url

        if not base_url:
            continue

        target = urllib.parse.urljoin(
            f"{base_url.rstrip('/')}/",
            path.lstrip("/"),
        )

        try:
            response = _fetch(target)
        except (urllib.error.URLError, OSError):
            continue

        if response["status"] in {200, 201, 204}:
            observations.append(
                _observation(
                    "a01_protected_route",
                    "authorized_active",
                    "possible_broken_access_control",
                    "high",
                    "Protected route is reachable without authentication",
                    "An explicitly protected route returned a successful unauthenticated response.",
                    {
                        "route": path,
                        "status": response["status"],
                        "url": target,
                    },
                    security_relevant=True,
                    alert=True,
                    alert_on_first=True,
                    mode="authorized_active",
                )
            )
        else:
            observations.append(
                _observation(
                    "a01_protected_route",
                    "authorized_active",
                    "protected_route_access_control_state",
                    "informational",
                    "Protected route access control checked",
                    "The explicitly protected route did not return a successful unauthenticated response.",
                    {
                        "route": path,
                        "status": response["status"],
                        "url": target,
                    },
                    security_relevant=False,
                    alert=False,
                    mode="authorized_active",
                )
            )

    return observations


def ingest_client_observations(
    application,
    source,
    observations,
):
    if source not in {"android", "windows"}:
        raise DetectionError("Unsupported client source.")

    normalized = []

    for item in observations or []:
        if not isinstance(item, dict):
            continue

        normalized.append(
            _observation(
                "client_observation",
                source,
                item.get("event_type", "client_security_observation"),
                item.get("severity", "informational"),
                item.get("title", f"{source.title()} security observation"),
                item.get("description", "Client security telemetry was received."),
                item.get("evidence", item.get("payload", {})),
                security_relevant=bool(
                    item.get("security_relevant", False)
                ),
                alert=bool(item.get("alert", False)),
                alert_on_first=bool(
                    item.get("alert_on_first", False)
                ),
                mode="client_telemetry",
                asset_id=item.get("asset_id"),
            )
        )

    return process_observations(
        application,
        normalized,
    )


def ingest_asset_findings(
    application,
    asset,
    findings,
    source="asset",
):
    if not asset or asset.application_id != application.id:
        raise DetectionError(
            "Asset does not belong to the application."
        )

    normalized = []

    for finding in findings or []:
        if not isinstance(finding, dict):
            continue

        normalized.append(
            _observation(
                "asset_finding",
                source,
                finding.get("event_type", "asset_security_finding"),
                finding.get("severity", "low"),
                finding.get("title", "Security finding from application asset"),
                finding.get(
                    "description",
                    "A security-relevant finding was derived from a protected asset.",
                ),
                finding.get("evidence", {}),
                security_relevant=True,
                alert=finding.get("alert", True),
                alert_on_first=finding.get("alert_on_first", True),
                mode="document_derived",
                asset_id=asset.id,
            )
        )

    return process_observations(
        application,
        normalized,
    )


def process_observations(application, observations):
    state = _application_state(application)
    state.setdefault("checks", {})
    state.setdefault("last_cycle_at", None)

    created_events = []
    created_alerts = []

    for observation in observations:
        check_id = observation["check_id"]
        evidence = observation["evidence"]
        fingerprint = _fingerprint(evidence)

        previous = state["checks"].get(check_id)
        previous_fingerprint = (
            previous.get("fingerprint")
            if isinstance(previous, dict)
            else None
        )

        first_observation = previous is None
        changed = (
            not first_observation
            and previous_fingerprint != fingerprint
        )

        current = {
            "fingerprint": fingerprint,
            "security_relevant": observation["security_relevant"],
            "severity": observation["severity"],
            "category": observation["category"],
            "event_type": observation["event_type"],
            "title": observation["title"],
            "description": observation["description"],
            "evidence": evidence,
            "source": observation["source"],
            "mode": observation["mode"],
            "asset_id": observation["asset_id"],
            "updated_at": utcnow().isoformat(),
        }

        state["checks"][check_id] = current

        should_record = (
            observation["security_relevant"]
            and (
                first_observation and observation["retain_on_first"]
                or changed
            )
        )

        should_alert = (
            observation["alert"]
            and (
                changed
                or (
                    first_observation
                    and observation["alert_on_first"]
                )
            )
        )

        event = None

        if should_record:
            event = Event(
                application_id=application.id,
                asset_id=observation["asset_id"],
                source=observation["source"],
                event_type=observation["event_type"],
                severity=observation["severity"],
                title=observation["title"],
                description=observation["description"],
                actor_identifier="darkops:detection",
                payload={
                    "check_id": check_id,
                    "category": observation["category"],
                    "mode": observation["mode"],
                    "fingerprint": fingerprint,
                    "changed": changed,
                    "first_observation": first_observation,
                    "evidence": evidence,
                },
                occurred_at=utcnow(),
            )

            db.session.add(event)
            created_events.append(event)

        if should_alert:
            alert = Alert(
                application_id=application.id,
                event_id=None,
                title=observation["title"],
                description=observation["description"],
                alert_type=observation["event_type"],
                severity=observation["severity"],
                status="open",
                first_seen_at=utcnow(),
                metadata={
                    "detection_check_id": check_id,
                    "source": observation["source"],
                    "mode": observation["mode"],
                    "fingerprint": fingerprint,
                    "changed": changed,
                },
            )

            db.session.add(alert)
            created_alerts.append(alert)

            if event:
                db.session.flush()
                alert.event_id = event.id

    state["last_cycle_at"] = utcnow().isoformat()
    _set_state(application, state)

    db.session.commit()

    return {
        "events_created": len(created_events),
        "alerts_created": len(created_alerts),
        "events": created_events,
        "alerts": created_alerts,
        "state": state,
    }


def run_detection_cycle(
    application,
    protected_routes=None,
    client_observations=None,
):
    if not application:
        raise DetectionError("Application is required.")

    application_type = (application.type or "").lower()
    observations = []

    if application_type in WEB_TYPES:
        for label, url in _get_url_pair(application):
            observations.extend(
                inspect_web_endpoint(
                    application,
                    label,
                    url,
                )
            )

        if protected_routes:
            observations.extend(
                inspect_protected_routes(
                    application,
                    protected_routes,
                )
            )

    elif application_type in ANDROID_TYPES:
        observations.extend(
            ingest_client_observations(
                application,
                "android",
                client_observations or [],
            )
        )

        if not client_observations:
            return {
                "status": "waiting_for_android_observations",
                "events_created": 0,
                "alerts_created": 0,
            }

    elif application_type in WINDOWS_TYPES:
        observations.extend(
            ingest_client_observations(
                application,
                "windows",
                client_observations or [],
            )
        )

        if not client_observations:
            return {
                "status": "waiting_for_windows_observations",
                "events_created": 0,
                "alerts_created": 0,
            }

    else:
        raise DetectionError(
            f"Unsupported application type: {application.type}"
        )

    return process_observations(
        application,
        observations,
    )
