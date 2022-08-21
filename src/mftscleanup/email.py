"""
Email handling code. We wrap it up in an Emailer instance for better testability.
"""


class Emailer:
    def __init__(self, from_address: str, email_host: str) -> None:
        assert isinstance(from_address, str), from_address
        assert isinstance(email_host, str), email_host
        self.from_address = from_address
        self.email_host = email_host

    def send_message(self, recipients: list[str], subject: str, body: str) -> None:
        raise NotImplementedError  # TODO
