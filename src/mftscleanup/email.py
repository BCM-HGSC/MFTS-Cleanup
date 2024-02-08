"""
Email handling code. We wrap it up in an Emailer instance for better testability.
"""
import os
import smtplib
import ssl
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class SMTPCredentials:
    """Class for SMTP credentials"""

    def __init__(self) -> None:
        self.host = os.environ.get("EMAIL_HOST")
        self.port = os.environ.get("EMAIL_PORT")
        self.username = os.environ.get("EMAIL_USERNAME")
        self.password = os.environ.get("EMAIL_PASSWORD")

    def __repr__(self):
        return f"SMTPCredentials(host={self.host}, port={self.port}, username={self.username})"


class Emailer:
    def __init__(self, from_address: str, email_host: str) -> None:
        assert isinstance(from_address, str), from_address
        assert isinstance(email_host, str), email_host
        self.from_address = from_address
        self.email_host = email_host

    def send_message(self, recipients: list[str], subject: str, body: str) -> None:
        # raise NotImplementedError  # TODO
        """Builds email message"""
        self.message = MIMEMultipart()
        self.message.attach(MIMEText(body, "html"))
        self.message["Subject"] = subject
        self.message["From"] = self.from_address
        self.message["To"] = ", ".join(recipients)
        self.credentials = SMTPCredentials()
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(self.credentials.host, self.credentials.port) as server:
                if self.credentials.username and self.credentials.password:
                    server.starttls(context=context)
                    server.login(self.credentials.username, self.credentials.password)
                server.send_message(self.message)
        except Exception:
            logger.exception("Unable to send email")
            return 1
        return 0
