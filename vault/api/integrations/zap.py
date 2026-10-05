import os
from urllib.parse import urljoin

import requests


class ZAPError(Exception):
    pass


class ZAPClient:
    def __init__(self, base_url=None, api_key=None, timeout=None):
        self.base_url = (
            base_url
            or os.getenv("ZAP_BASE_URL")
            or "http://127.0.0.1:8080"
        ).rstrip("/") + "/"

        self.api_key = api_key or os.getenv("ZAP_API_KEY")
        self.timeout = timeout or int(
            os.getenv("ZAP_TIMEOUT_SECONDS", "30")
        )

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })

    def _request(self, component, kind, operation, params=None):
        params = dict(params or {})

        if self.api_key:
            params["apikey"] = self.api_key

        url = urljoin(
            self.base_url,
            f"JSON/{component}/{kind}/{operation}/",
        )

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ZAPError(
                f"ZAP request failed: {exc}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise ZAPError(
                "ZAP returned a non-JSON response."
            ) from exc

        if isinstance(payload, dict) and payload.get("code") == "error":
            raise ZAPError(
                payload.get("message")
                or payload.get("detail")
                or "ZAP API error."
            )

        return payload

    def health(self):
        return self._request(
            "core",
            "view",
            "version",
        )

    def spider(
        self,
        url,
        recurse=True,
        context_name=None,
        subtree_only=False,
        max_children=None,
    ):
        if not url:
            raise ZAPError("Spider target URL is required.")

        params = {
            "url": url,
            "recurse": str(bool(recurse)).lower(),
            "subtreeOnly": str(bool(subtree_only)).lower(),
        }

        if context_name:
            params["contextName"] = context_name

        if max_children is not None:
            params["maxChildren"] = max_children

        return self._request(
            "spider",
            "action",
            "scan",
            params,
        )

    def spider_status(self, scan_id):
        if scan_id is None:
            raise ZAPError("Spider scan ID is required.")

        return self._request(
            "spider",
            "view",
            "status",
            {"scanId": scan_id},
        )

    def spider_results(self, scan_id):
        if scan_id is None:
            raise ZAPError("Spider scan ID is required.")

        return self._request(
            "spider",
            "view",
            "results",
            {"scanId": scan_id},
        )

    def stop_spider(self, scan_id):
        if scan_id is None:
            raise ZAPError("Spider scan ID is required.")

        return self._request(
            "spider",
            "action",
            "stop",
            {"scanId": scan_id},
        )

    def active_scan(
        self,
        url,
        recurse=True,
        in_scope_only=True,
        scan_policy_name=None,
    ):
        if not url:
            raise ZAPError("Active scan target URL is required.")

        params = {
            "url": url,
            "recurse": str(bool(recurse)).lower(),
            "inScopeOnly": str(bool(in_scope_only)).lower(),
        }

        if scan_policy_name:
            params["scanPolicyName"] = scan_policy_name

        return self._request(
            "ascan",
            "action",
            "scan",
            params,
        )

    def active_scan_status(self, scan_id):
        if scan_id is None:
            raise ZAPError("Active scan ID is required.")

        return self._request(
            "ascan",
            "view",
            "status",
            {"scanId": scan_id},
        )

    def stop_active_scan(self, scan_id):
        if scan_id is None:
            raise ZAPError("Active scan ID is required.")

        return self._request(
            "ascan",
            "action",
            "stop",
            {"scanId": scan_id},
        )

    def passive_scan_status(self):
        return self._request(
            "pscan",
            "view",
            "recordsToScan",
        )

    def alerts(
        self,
        base_url=None,
        start=0,
        count=100,
        risk_id=None,
    ):
        params = {
            "start": start,
            "count": count,
        }

        if base_url:
            params["baseurl"] = base_url

        if risk_id is not None:
            params["riskId"] = risk_id

        return self._request(
            "core",
            "view",
            "alerts",
            params,
        )

    def alert_summary(self, base_url=None):
        params = {}

        if base_url:
            params["baseurl"] = base_url

        return self._request(
            "alert",
            "view",
            "alertsSummary",
            params,
        )


def get_zap_client():
    return ZAPClient()
