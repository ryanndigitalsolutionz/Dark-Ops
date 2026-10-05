import os

import requests


class MobSFError(Exception):
    pass


class MobSFClient:
    def __init__(self, base_url=None, api_key=None, timeout=None):
        self.base_url = (
            base_url
            or os.getenv("MOBSF_BASE_URL")
            or "http://127.0.0.1:8000"
        ).rstrip("/")

        self.api_key = api_key or os.getenv("MOBSF_API_KEY")
        self.timeout = timeout or int(
            os.getenv("MOBSF_TIMEOUT_SECONDS", "60")
        )

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })

    def _headers(self):
        if not self.api_key:
            raise MobSFError(
                "MOBSF_API_KEY is not configured."
            )

        return {
            "Authorization": self.api_key,
            "Accept": "application/json",
        }

    def _request(
        self,
        method,
        endpoint,
        *,
        data=None,
        files=None,
        timeout=None,
    ):
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method,
                url,
                headers=self._headers(),
                data=data,
                files=files,
                timeout=timeout or self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise MobSFError(
                f"MobSF request failed: {exc}"
            ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise MobSFError(
                "MobSF returned a non-JSON response."
            ) from exc

    def health(self):
        try:
            response = self.session.get(
                f"{self.base_url}/",
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise MobSFError(
                f"MobSF health check failed: {exc}"
            ) from exc

        return {
            "available": True,
            "status_code": response.status_code,
        }

    def upload(self, file_path):
        if not file_path:
            raise MobSFError("MobSF upload file is required.")

        try:
            with open(file_path, "rb") as file:
                response = self.session.post(
                    f"{self.base_url}/api/v1/upload",
                    headers=self._headers(),
                    files={
                        "file": (
                            os.path.basename(file_path),
                            file,
                            "application/octet-stream",
                        )
                    },
                    timeout=self.timeout,
                )
                response.raise_for_status()
        except OSError as exc:
            raise MobSFError(
                f"Unable to open MobSF upload: {exc}"
            ) from exc
        except requests.RequestException as exc:
            raise MobSFError(
                f"MobSF upload failed: {exc}"
            ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise MobSFError(
                "MobSF returned a non-JSON upload response."
            ) from exc

    def scan(
        self,
        file_hash,
        scan_type="apk",
        re_scan=False,
    ):
        if not file_hash:
            raise MobSFError("MobSF file hash is required.")

        return self._request(
            "POST",
            "/api/v1/scan",
            data={
                "hash": file_hash,
                "scan_type": scan_type,
                "re_scan": str(bool(re_scan)).lower(),
            },
        )

    def get_report(self, file_hash):
        if not file_hash:
            raise MobSFError("MobSF file hash is required.")

        return self._request(
            "POST",
            "/api/v1/report_json",
            data={"hash": file_hash},
        )

    def get_scorecard(self, file_hash):
        if not file_hash:
            raise MobSFError("MobSF file hash is required.")

        return self._request(
            "POST",
            "/api/v1/scorecard",
            data={"hash": file_hash},
        )

    def delete_scan(self, file_hash):
        if not file_hash:
            raise MobSFError("MobSF file hash is required.")

        return self._request(
            "POST",
            "/api/v1/delete_scan",
            data={"hash": file_hash},
        )


def get_mobsf_client():
    return MobSFClient()
