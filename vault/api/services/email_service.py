import base64
import os
import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage

import requests
from flask import current_app


class EmailServiceError(Exception):
    pass


class EmailProvider(ABC):
    name = None

    @abstractmethod
    def send(self, **kwargs):
        raise NotImplementedError


class BrevoEmailProvider(EmailProvider):
    name = "brevo"
    endpoint = "https://api.brevo.com/v3/smtp/email"

    def __init__(self):
        self.api_key = (
            current_app.config.get("BREVO_API_KEY")
            or os.getenv("BREVO_API_KEY")
        )

        if not self.api_key:
            raise EmailServiceError(
                "BREVO_API_KEY is not configured."
            )

        self.timeout = int(
            current_app.config.get(
                "BREVO_TIMEOUT_SECONDS",
                15,
            )
        )

    def send(
        self,
        to,
        subject=None,
        html_content=None,
        text_content=None,
        sender_email=None,
        sender_name=None,
        reply_to=None,
        template_id=None,
        params=None,
        attachments=None,
        tags=None,
    ):
        if not to:
            raise EmailServiceError(
                "At least one recipient is required."
            )

        sender_email = (
            sender_email
            or current_app.config.get("BREVO_SENDER_EMAIL")
            or os.getenv("BREVO_SENDER_EMAIL")
        )

        sender_name = (
            sender_name
            or current_app.config.get("BREVO_SENDER_NAME")
            or os.getenv("BREVO_SENDER_NAME", "DarkOps")
        )

        if not sender_email:
            raise EmailServiceError(
                "BREVO_SENDER_EMAIL is not configured."
            )

        payload = {
            "sender": {
                "email": sender_email,
                "name": sender_name,
            },
            "to": _normalize_recipients(to),
        }

        if template_id is not None:
            payload["templateId"] = int(template_id)

            if params is not None:
                payload["params"] = params

        else:
            if not subject:
                raise EmailServiceError(
                    "Email subject is required."
                )

            if not html_content and not text_content:
                raise EmailServiceError(
                    "HTML content or text content is required."
                )

            payload["subject"] = subject

            if html_content:
                payload["htmlContent"] = html_content

            if text_content:
                payload["textContent"] = text_content

        if reply_to:
            payload["replyTo"] = _normalize_recipient(
                reply_to
            )

        if attachments:
            payload["attachment"] = _normalize_attachments(
                attachments
            )

        if tags:
            payload["tags"] = tags

        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }

        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise EmailServiceError(
                "Brevo could not be reached."
            ) from error

        if not 200 <= response.status_code < 300:
            try:
                detail = response.json().get(
                    "message",
                    response.text,
                )
            except ValueError:
                detail = response.text

            raise EmailServiceError(
                f"Brevo rejected the email: {detail}"
            )

        try:
            return response.json()
        except ValueError:
            return {
                "status": "sent",
                "provider": self.name,
            }


class GmailSMTPProvider(EmailProvider):
    name = "gmail_smtp"

    def __init__(self):
        self.username = (
            current_app.config.get("GMAIL_SMTP_EMAIL")
            or os.getenv("GMAIL_SMTP_EMAIL")
        )

        self.password = (
            current_app.config.get(
                "GMAIL_SMTP_APP_PASSWORD"
            )
            or os.getenv("GMAIL_SMTP_APP_PASSWORD")
        )

        self.host = (
            current_app.config.get(
                "GMAIL_SMTP_HOST"
            )
            or os.getenv(
                "GMAIL_SMTP_HOST",
                "smtp.gmail.com",
            )
        )

        self.port = int(
            current_app.config.get(
                "GMAIL_SMTP_PORT"
            )
            or os.getenv(
                "GMAIL_SMTP_PORT",
                "587",
            )
        )

        if not self.username or not self.password:
            raise EmailServiceError(
                "Gmail SMTP credentials are not configured."
            )

    def send(
        self,
        to,
        subject,
        html_content=None,
        text_content=None,
        sender_email=None,
        sender_name=None,
        reply_to=None,
        attachments=None,
        **_,
    ):
        if not to:
            raise EmailServiceError(
                "At least one recipient is required."
            )

        if not subject:
            raise EmailServiceError(
                "Email subject is required."
            )

        sender_email = (
            sender_email
            or current_app.config.get(
                "GMAIL_SENDER_EMAIL"
            )
            or self.username
        )

        sender_name = (
            sender_name
            or current_app.config.get(
                "GMAIL_SENDER_NAME"
            )
            or os.getenv(
                "GMAIL_SENDER_NAME",
                "DarkOps",
            )
        )

        message = EmailMessage()

        message["From"] = (
            f"{sender_name} <{sender_email}>"
        )

        message["To"] = ", ".join(
            _recipient_address(item)
            for item in _normalize_recipients(to)
        )

        message["Subject"] = subject

        if reply_to:
            message["Reply-To"] = _recipient_address(
                _normalize_recipient(reply_to)
            )

        plain = (
            text_content
            or _strip_html(
                html_content or ""
            )
        )

        message.set_content(plain)

        if html_content:
            message.add_alternative(
                html_content,
                subtype="html",
            )

        for attachment in attachments or []:
            _attach_smtp_file(
                message,
                attachment,
            )

        try:
            with smtplib.SMTP(
                self.host,
                self.port,
                timeout=15,
            ) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(
                    self.username,
                    self.password,
                )
                smtp.send_message(message)

        except (
            smtplib.SMTPException,
            OSError,
        ) as error:
            raise EmailServiceError(
                "Gmail SMTP could not send the email."
            ) from error

        return {
            "status": "sent",
            "provider": self.name,
        }


def _normalize_recipient(recipient):
    if isinstance(recipient, str):
        return {
            "email": recipient,
        }

    if not isinstance(recipient, dict):
        raise EmailServiceError(
            "Invalid email recipient."
        )

    email = recipient.get("email")

    if not email:
        raise EmailServiceError(
            "Recipient email is required."
        )

    result = {
        "email": email,
    }

    if recipient.get("name"):
        result["name"] = recipient["name"]

    return result


def _normalize_recipients(recipients):
    if isinstance(recipients, (str, dict)):
        recipients = [recipients]

    if not isinstance(recipients, (list, tuple)):
        raise EmailServiceError(
            "Recipients must be a collection."
        )

    return [
        _normalize_recipient(recipient)
        for recipient in recipients
    ]


def _recipient_address(recipient):
    name = recipient.get("name")
    email = recipient["email"]

    if name:
        return f"{name} <{email}>"

    return email


def _normalize_attachments(attachments):
    normalized = []

    for attachment in attachments:
        if not isinstance(attachment, dict):
            raise EmailServiceError(
                "Invalid email attachment."
            )

        item = {}

        if attachment.get("url"):
            item["url"] = attachment["url"]

        elif attachment.get("content"):
            content = attachment["content"]

            if isinstance(content, bytes):
                content = base64.b64encode(
                    content
                ).decode("ascii")

            item["content"] = content

        else:
            raise EmailServiceError(
                "Attachment requires a URL or content."
            )

        if attachment.get("name"):
            item["name"] = attachment["name"]

        normalized.append(item)

    return normalized


def _attach_smtp_file(message, attachment):
    filename = attachment.get("name")

    if not filename:
        raise EmailServiceError(
            "SMTP attachment filename is required."
        )

    content = attachment.get("content")

    if content is None:
        raise EmailServiceError(
            "SMTP attachments currently require file content."
        )

    if isinstance(content, str):
        content = content.encode()

    maintype, subtype = (
        attachment.get(
            "mime_type",
            "application/octet-stream",
        ).split("/", 1)
    )

    message.add_attachment(
        content,
        maintype=maintype,
        subtype=subtype,
        filename=filename,
    )


def _strip_html(html):
    import re

    return re.sub(
        r"<[^>]+>",
        "",
        html,
    )


class EmailService:
    def __init__(self):
        self.primary = BrevoEmailProvider()
        self.backup = None

        if (
            current_app.config.get(
                "GMAIL_SMTP_EMAIL"
            )
            or os.getenv("GMAIL_SMTP_EMAIL")
        ):
            self.backup = GmailSMTPProvider()

    def send(
        self,
        to,
        subject,
        html_content=None,
        text_content=None,
        sender_email=None,
        sender_name=None,
        reply_to=None,
        template_id=None,
        params=None,
        attachments=None,
        tags=None,
        use_backup=True,
    ):
        try:
            return self.primary.send(
                to=to,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                sender_email=sender_email,
                sender_name=sender_name,
                reply_to=reply_to,
                template_id=template_id,
                params=params,
                attachments=attachments,
                tags=tags,
            )

        except EmailServiceError as primary_error:
            if not use_backup or not self.backup:
                raise

            try:
                return self.backup.send(
                    to=to,
                    subject=subject,
                    html_content=html_content,
                    text_content=text_content,
                    sender_email=sender_email,
                    sender_name=sender_name,
                    reply_to=reply_to,
                    attachments=attachments,
                )

            except EmailServiceError as backup_error:
                raise EmailServiceError(
                    f"Primary email provider failed: "
                    f"{primary_error}; backup provider failed: "
                    f"{backup_error}"
                ) from backup_error


def get_email_service():
    return EmailService()


def send_email(**kwargs):
    return get_email_service().send(
        **kwargs
    )
