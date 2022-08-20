"""
Email handling code. We wrap it up in an Emailer instance for better testability.
"""


class Emailer:
    def __init__(self, from_address, email_host) -> None:
        self.from_address = from_address
        self.email_host = email_host

    def send_message(self, recipients: list[str], subject: str, body: str) -> None:
        raise NotImplementedError  # TODO
