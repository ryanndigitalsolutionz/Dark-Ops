import hashlib
import hmac
import json
import os
import uuid
from abc import ABC, abstractmethod

import requests
from flask import current_app


class PaymentProviderError(Exception):
    pass


class PaymentProvider(ABC):
    name = None

    @abstractmethod
    def initialize_transaction(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def verify_transaction(self, reference):
        raise NotImplementedError

    @abstractmethod
    def create_plan(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create_subscription(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_subscription(self, code):
        raise NotImplementedError

    @abstractmethod
    def disable_subscription(self, code, token):
        raise NotImplementedError

    @abstractmethod
    def create_refund(self, **kwargs):
        raise NotImplementedError


class PaystackProvider(PaymentProvider):
    name = "paystack"
    base_url = "https://api.paystack.co"

    def __init__(self):
        self.secret_key = (
            current_app.config.get("PAYSTACK_SECRET_KEY")
            or os.getenv("PAYSTACK_SECRET_KEY")
        )

        if not self.secret_key:
            raise PaymentProviderError(
                "PAYSTACK_SECRET_KEY is not configured."
            )

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"

        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                timeout=current_app.config.get(
                    "PAYMENT_PROVIDER_TIMEOUT_SECONDS",
                    15,
                ),
                **kwargs,
            )
        except requests.RequestException as error:
            raise PaymentProviderError(
                "Unable to reach the payment provider."
            ) from error

        try:
            payload = response.json()
        except ValueError:
            raise PaymentProviderError(
                "Payment provider returned an invalid response."
            )

        if response.status_code >= 400 or not payload.get("status"):
            raise PaymentProviderError(
                payload.get(
                    "message",
                    "Payment provider request failed.",
                )
            )

        return payload.get("data", payload)

    @staticmethod
    def _reference():
        return (
            f"DO-{uuid.uuid4().hex.upper()}"
        )

    @staticmethod
    def _metadata(metadata):
        if metadata is None:
            return None

        if isinstance(metadata, str):
            return metadata

        try:
            return json.dumps(
                metadata,
                separators=(",", ":"),
            )
        except (TypeError, ValueError) as error:
            raise PaymentProviderError(
                "Invalid payment metadata."
            ) from error

    def initialize_transaction(
        self,
        email,
        amount,
        currency=None,
        reference=None,
        plan_code=None,
        channels=None,
        callback_url=None,
        metadata=None,
        invoice_limit=None,
    ):
        if not email:
            raise PaymentProviderError(
                "Customer email is required."
            )

        if amount is None and not plan_code:
            raise PaymentProviderError(
                "Amount or plan code is required."
            )

        payload = {
            "email": email,
            "reference": reference or self._reference(),
        }

        if amount is not None:
            payload["amount"] = str(amount)

        if currency:
            payload["currency"] = currency

        if plan_code:
            payload["plan"] = plan_code

        if channels:
            payload["channels"] = channels

        if callback_url:
            payload["callback_url"] = callback_url

        if metadata is not None:
            payload["metadata"] = self._metadata(
                metadata
            )

        if invoice_limit is not None:
            payload["invoice_limit"] = invoice_limit

        return self._request(
            "POST",
            "/transaction/initialize",
            json=payload,
        )

    def verify_transaction(self, reference):
        if not reference:
            raise PaymentProviderError(
                "Transaction reference is required."
            )

        return self._request(
            "GET",
            f"/transaction/verify/{reference}",
        )

    def create_plan(
        self,
        name,
        amount,
        interval,
        currency=None,
        description=None,
        invoice_limit=None,
    ):
        if not name:
            raise PaymentProviderError(
                "Plan name is required."
            )

        payload = {
            "name": name,
            "amount": int(amount),
            "interval": interval,
        }

        if currency:
            payload["currency"] = currency

        if description:
            payload["description"] = description

        if invoice_limit is not None:
            payload["invoice_limit"] = invoice_limit

        return self._request(
            "POST",
            "/plan",
            json=payload,
        )

    def update_plan(
        self,
        plan_code,
        name=None,
        amount=None,
        interval=None,
        description=None,
        invoice_limit=None,
        update_existing_subscriptions=None,
    ):
        if not plan_code:
            raise PaymentProviderError(
                "Plan code is required."
            )

        payload = {}

        if name is not None:
            payload["name"] = name

        if amount is not None:
            payload["amount"] = int(amount)

        if interval is not None:
            payload["interval"] = interval

        if description is not None:
            payload["description"] = description

        if invoice_limit is not None:
            payload["invoice_limit"] = invoice_limit

        if update_existing_subscriptions is not None:
            payload[
                "update_existing_subscriptions"
            ] = update_existing_subscriptions

        return self._request(
            "PUT",
            f"/plan/{plan_code}",
            json=payload,
        )

    def create_subscription(
        self,
        customer,
        plan_code,
        authorization=None,
        start_date=None,
    ):
        if not customer:
            raise PaymentProviderError(
                "Customer identifier is required."
            )

        if not plan_code:
            raise PaymentProviderError(
                "Plan code is required."
            )

        payload = {
            "customer": customer,
            "plan": plan_code,
        }

        if authorization:
            payload["authorization"] = authorization

        if start_date:
            payload["start_date"] = start_date

        return self._request(
            "POST",
            "/subscription",
            json=payload,
        )

    def get_subscription(self, code):
        if not code:
            raise PaymentProviderError(
                "Subscription code is required."
            )

        return self._request(
            "GET",
            f"/subscription/{code}",
        )

    def disable_subscription(self, code, token):
        if not code or not token:
            raise PaymentProviderError(
                "Subscription code and token are required."
            )

        return self._request(
            "POST",
            "/subscription/disable",
            json={
                "code": code,
                "token": token,
            },
        )

    def enable_subscription(self, code, token):
        if not code or not token:
            raise PaymentProviderError(
                "Subscription code and token are required."
            )

        return self._request(
            "POST",
            "/subscription/enable",
            json={
                "code": code,
                "token": token,
            },
        )

    def create_refund(
        self,
        transaction,
        amount=None,
        currency=None,
        customer_note=None,
        merchant_note=None,
    ):
        if not transaction:
            raise PaymentProviderError(
                "Transaction reference or ID is required."
            )

        payload = {
            "transaction": transaction,
        }

        if amount is not None:
            payload["amount"] = int(amount)

        if currency:
            payload["currency"] = currency

        if customer_note:
            payload["customer_note"] = customer_note

        if merchant_note:
            payload["merchant_note"] = merchant_note

        return self._request(
            "POST",
            "/refund",
            json=payload,
        )

    def generate_subscription_manage_link(self, code):
        if not code:
            raise PaymentProviderError(
                "Subscription code is required."
            )

        return self._request(
            "GET",
            f"/subscription/{code}/manage/link",
        )

    def verify_webhook_signature(
        self,
        raw_body,
        signature,
    ):
        if not raw_body or not signature:
            return False

        expected = hmac.new(
            self.secret_key.encode("utf-8"),
            raw_body,
            hashlib.sha512,
        ).hexdigest()

        return hmac.compare_digest(
            expected,
            signature,
        )


def get_payment_provider(name=None):
    provider_name = (
        name
        or current_app.config.get(
            "PAYMENT_PROVIDER"
        )
        or os.getenv(
            "PAYMENT_PROVIDER",
            "paystack",
        )
    ).strip().lower()

    providers = {
        "paystack": PaystackProvider,
    }

    provider = providers.get(provider_name)

    if not provider:
        raise PaymentProviderError(
            f"Unsupported payment provider: {provider_name}"
        )

    return provider()
