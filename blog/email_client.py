"""Lightweight SMTP email client that reads configuration from Django settings."""

from __future__ import annotations

import smtplib
from email.message import EmailMessage
from ssl import create_default_context
from typing import Iterable

from django.conf import settings


class EmailDeliveryError(Exception):
    """Raised when the SMTP server cannot send the email."""


def _normalize_recipients(names: Iterable[str] | str | None) -> list[str]:
    if not names:
        return []
    if isinstance(names, str):
        return [names]
    return list(names)


class SMTPEmailClient:
    """Send emails through Python's built-in :mod:`smtplib`.

    The client honors the Django settings defined in :mod:`blogapi.settings`.
    """

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        use_tls: bool | None = None,
        use_ssl: bool | None = None,
        timeout: int | None = None,
    ):
        self.host = host or settings.EMAIL_HOST
        self.port = port or settings.EMAIL_PORT
        self.username = username or settings.EMAIL_HOST_USER
        self.password = password or settings.EMAIL_HOST_PASSWORD
        self.use_tls = use_tls if use_tls is not None else settings.EMAIL_USE_TLS
        self.use_ssl = use_ssl if use_ssl is not None else settings.EMAIL_USE_SSL
        self.timeout = timeout or settings.EMAIL_TIMEOUT

    def _connect(self) -> smtplib.SMTP:
        context = create_default_context()
        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.host, self.port, timeout=self.timeout, context=context)
        else:
            server = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            if self.use_tls:
                server.starttls(context=context)

        if self.username:
            server.login(self.username, self.password)

        return server

    def send(
        self,
        subject: str,
        body: str,
        *,
        to: Iterable[str] | str,
        html_body: str | None = None,
        from_email: str | None = None,
        cc: Iterable[str] | str | None = None,
        bcc: Iterable[str] | str | None = None,
    ) -> None:
        recipients = _normalize_recipients(to)
        cc_list = _normalize_recipients(cc)
        bcc_list = _normalize_recipients(bcc)
        if not recipients and not cc_list and not bcc_list:
            raise EmailDeliveryError('No recipient addresses were provided')

        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = from_email or settings.DEFAULT_FROM_EMAIL
        message['To'] = ', '.join(recipients)
        if cc_list:
            message['Cc'] = ', '.join(cc_list)

        message.set_content(body)
        if html_body:
            message.add_alternative(html_body, subtype='html')

        try:
            server = self._connect()
            server.send_message(message, from_addr=message['From'], to_addrs=[*recipients, *cc_list, *bcc_list])
        except smtplib.SMTPException as exc:
            raise EmailDeliveryError('Failed to deliver email') from exc
        finally:
            try:
                if 'server' in locals():
                    server.quit()
            except smtplib.SMTPException:
                pass


def send_email(*, subject: str, body: str, to: Iterable[str] | str, **kwargs) -> None:
    """Shorthand helper that uses the default client settings to send a message."""

    SMTPEmailClient().send(subject, body, to=to, **kwargs)
