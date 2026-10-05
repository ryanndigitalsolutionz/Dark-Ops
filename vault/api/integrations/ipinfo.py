import os

import requests


class IPInfoError(Exception):
    pass


class IPInfoClient:
    def __init__(self, base_url=None, api_token=None, timeout=None):
        self.base_url = (
            base_url
            or os.getenv("IPINFO_BASE_URL")
            or "https://api.ipinfo.io"
        ).rstrip("/")

        self.api_token = (
            api_token
            or os.getenv("IPINFO_API_TOKEN")
            or os.getenv("IPINFO_TOKEN")
        )

        self.timeout = timeout or int(
            os.getenv("IPINFO_TIMEOUT_SECONDS", "15")
        )

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })

    def _request(self, endpoint, params=None):
        if not self.api_token:
            raise IPInfoError(
                "IPINFO_API_TOKEN is not configured."
            )

        request_params = dict(params or {})
        request_params["token"] = self.api_token

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.get(
                url,
                params=request_params,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise IPInfoError(
                f"IPinfo request failed: {exc}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise IPInfoError(
                "IPinfo returned invalid JSON."
            ) from exc

        if isinstance(payload, dict) and payload.get("error"):
            error = payload["error"]

            if isinstance(error, dict):
                message = error.get(
                    "message",
                    "IPinfo API error."
                )
            else:
                message = str(error)

            raise IPInfoError(message)

        return payload

    def lookup(self, ip_address):
        if not ip_address:
            raise IPInfoError(
                "IP address is required."
            )

        return self._request(
            f"lookup/{ip_address.strip()}"
        )

    def lookup_me(self):
        return self._request("lookup/me")

    def get_privacy(self, ip_address):
        if not ip_address:
            raise IPInfoError(
                "IP address is required."
            )

        return self._request(
            f"lookup/{ip_address.strip()}/anonymous"
        )

    def get_privacy_me(self):
        return self._request(
            "lookup/me/anonymous"
        )

    def get_asn(self, asn):
        if not asn:
            raise IPInfoError(
                "ASN is required."
            )

        normalized = asn.strip().upper()

        if not normalized.startswith("AS"):
            normalized = f"AS{normalized}"

        return self._request(
            f"lookup/{normalized}"
        )

    def health(self):
        return {
            "available": True,
            "response": self.lookup_me(),
        }


def get_ipinfo_client():
    return IPInfoClient()
