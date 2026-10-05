import os

import requests


class RESTCountriesError(Exception):
    pass


class RESTCountriesClient:
    def __init__(self, base_url=None, api_key=None, timeout=None):
        self.base_url = (
            base_url
            or os.getenv("REST_COUNTRIES_BASE_URL")
            or "https://api.restcountries.com/countries/v5"
        ).rstrip("/")

        self.api_key = api_key or os.getenv("REST_COUNTRIES_API_KEY")

        self.timeout = timeout or int(
            os.getenv("REST_COUNTRIES_TIMEOUT_SECONDS", "15")
        )

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })

    def _headers(self):
        if not self.api_key:
            raise RESTCountriesError(
                "REST_COUNTRIES_API_KEY is not configured."
            )

        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def _request(self, endpoint="", params=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if endpoint else self.base_url

        try:
            response = self.session.get(
                url,
                headers=self._headers(),
                params=params or {},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RESTCountriesError(
                f"REST Countries request failed: {exc}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise RESTCountriesError(
                "REST Countries returned invalid JSON."
            ) from exc

        if payload.get("errors"):
            errors = payload["errors"]

            if isinstance(errors, list) and errors:
                message = errors[0].get(
                    "message",
                    "REST Countries API error."
                )
            else:
                message = "REST Countries API error."

            raise RESTCountriesError(message)

        return payload

    def get_country_by_alpha2(self, alpha2):
        if not alpha2:
            raise RESTCountriesError(
                "Country alpha-2 code is required."
            )

        return self._request(
            f"codes.alpha_2/{alpha2.strip().upper()}",
            params={
                "response_fields": (
                    "names.common,"
                    "names.official,"
                    "codes.alpha_2,"
                    "codes.alpha_3,"
                    "capital,"
                    "region,"
                    "subregion,"
                    "continents,"
                    "languages,"
                    "currencies,"
                    "timezones,"
                    "flag.emoji"
                )
            },
        )

    def get_country_by_name(self, name):
        if not name:
            raise RESTCountriesError(
                "Country name is required."
            )

        return self._request(
            f"names.common/{name.strip()}",
            params={
                "response_fields": (
                    "names.common,"
                    "names.official,"
                    "codes.alpha_2,"
                    "codes.alpha_3,"
                    "capital,"
                    "region,"
                    "subregion,"
                    "continents,"
                    "languages,"
                    "currencies,"
                    "timezones,"
                    "flag.emoji"
                )
            },
        )

    def search(self, query, limit=25):
        if not query:
            raise RESTCountriesError(
                "Country search query is required."
            )

        limit = max(1, min(int(limit), 100))

        return self._request(
            "",
            params={
                "q": query.strip(),
                "limit": limit,
                "response_fields": (
                    "names.common,"
                    "names.official,"
                    "codes.alpha_2,"
                    "codes.alpha_3,"
                    "region,"
                    "subregion,"
                    "continents,"
                    "flag.emoji"
                )
            },
        )

    def get_countries_by_region(self, region, limit=100):
        if not region:
            raise RESTCountriesError(
                "Country region is required."
            )

        limit = max(1, min(int(limit), 100))

        return self._request(
            "",
            params={
                "region": region.strip(),
                "limit": limit,
                "response_fields": (
                    "names.common,"
                    "codes.alpha_2,"
                    "codes.alpha_3,"
                    "region,"
                    "subregion,"
                    "continents,"
                    "flag.emoji"
                )
            },
        )

    def health(self):
        response = self.search("Kenya", limit=1)

        return {
            "available": True,
            "response": response,
        }


def get_rest_countries_client():
    return RESTCountriesClient()
