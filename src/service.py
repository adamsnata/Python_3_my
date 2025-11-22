import copy
from datetime import datetime

from src.email import Email
from src.status import Status


class EmailService():

    def __init__(self, email: Email):
        self.email = email

    def add_send_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def send_email(self) -> list[Email]:
        sent_emails: list[Email] = []

        for recipient in self.email.recipients:
            msg_copy = copy.deepcopy(self.email)

            # один получатель
            msg_copy.recipients = [recipient]

            # отправитель должен быть указан явно
            msg_copy.sender = self.email.sender

            # дата через метод
            msg_copy.date = self.add_send_date()

            # статус
            if self.email.status == Status.READY:
                msg_copy.status = Status.SENT
            else:
                msg_copy.status = Status.FAILED

            sent_emails.append(msg_copy)

        return sent_emails


class LoggingEmailService(EmailService):
    LOG_FILE = "send.log"

    def send_email(self) -> list[Email]:
        # вызываем логику родителя
        sent_emails = super().send_email()

        # пишем в лог
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            for msg in sent_emails:
                sender = msg.sender.masked
                recipient = msg.recipients[0].masked
                status = msg.status
                date = msg.date  # строка "YYYY-MM-DD"
                f.write(f"{date} | From: {sender} | To: {recipient} | Status: {status}\n")

        return sent_emails
