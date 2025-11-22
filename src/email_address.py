from __future__ import annotations

from dataclasses import dataclass


@dataclass()
class EmailAddress:
    """
    – Класс инкапсулирует email-адрес с методами:
    – Нормализация: приведение к нижнему регистру и обрезка пробелов.
    – Валидация: адрес должен содержать @ и заканчиваться на .com/.ru/.net. Невалидный адрес вызывает ValueError.
    – Маскированный вывод: свойство masked (первые_2_символа + "***@" + домен).
    – Подготовка Письма (Email.prepare()) - перед отправкой письмо должно быть подготовлено:
    – Очистка: subject и body очищаются от лишних пробелов и переносов.
    – Валидность: Если тема, тело, получатель и отправитель непустые → статус READY, иначе INVALID.
    – Short Body: Метод add_short_body() формирует сокращённую версию тела.
    – Вывод: Метод repr должен использовать маскированный адрес отправителя и список получателей через запятую.
    """

    def __init__(self, address: str):
        self._address = address
        self._check_correct_email()

    def normalize_address(self) -> str:
        return self._address.strip().lower()

    def _check_correct_email(self):
        if "@" not in self.address or not self.address.endswith((".com", ".ru", ".net")):
            raise ValueError("Invalid email address")

    @property
    def address(self) -> str:
        return self.normalize_address()

    @property
    def masked(self) -> str:
        local, _, domain = self.address.partition("@")
        return f"{local[:2]}***@{domain}"

