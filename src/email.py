from dataclasses import dataclass
from typing import Optional

from src.email_address import EmailAddress
from src.status import Status


@dataclass(slots=True)
class Email:
    subject: str
    body: str
    sender: EmailAddress
    recipients: list[EmailAddress] | EmailAddress
    date: Optional[str] = None
    short_body: Optional[str] = None
    status: Status = Status.DRAFT

    def __post_init__(self):
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]

    def get_recipients_str(self) -> str:
        return ", ".join(r.masked for r in self.recipients)

    def clean_data(self) -> "Email":
        self.subject = self.clean_text(self.subject)
        self.body = self.clean_text(self.body)
        return self

    def is_valid_fields(self) -> bool:
        return bool(self.subject and self.body)

    def clean_text(self, text: str) -> str:
        return " ".join(text.replace("\t", " ").replace("\n", " ").split())

    def add_short_body(self, n: int = 10) -> "Email":
        if self.body:
            self.short_body = (
                self.body[:n] + "..." if len(self.body) > n else self.body
            )
        return self

    def prepare(self) -> "Email":
        self.clean_data()

        if self.is_valid_fields() and self.sender and self.recipients:
            self.status = Status.READY
        else:
            self.status = Status.INVALID

        self.add_short_body()
        return self

    def __repr__(self):
        recipients_str = self.get_recipients_str()
        return (
                f"Status: {self.status}\n"
                f"Кому: {recipients_str}\n"
                f"От: {self.sender.masked}\n"
                f"Тема: {self.subject}, дата {self.date}\n"
                f"{self.short_body or self.body}"
            )


