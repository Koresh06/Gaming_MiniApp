from typing import Protocol
from uuid import UUID


class StarsPaymentServiceBase(Protocol):
    """
    Интерфейс сервиса Telegram Stars.
    """

    async def create_payment(self, tg_id: int, amount: int, bet_uuid: UUID) -> str:
        """
        Создать инвойс на списание Stars.
        Возвращает telegram_invoice_id.
        """
        ...

    async def create_payout(self, tg_id: int, amount: int, round_uuid: UUID) -> str:
        """
        Создать выплату Stars.
        Возвращает telegram_payout_id.
        """
        ...

    async def process_payment_callback(self, bet_uuid: UUID, status: str, tx_id: str):
        """
        Обработка payment callback.
        """
        ...

    async def process_payout_callback(self, payout_uuid: UUID, status: str, tx_id: str):
        """
        Обработка payout callback.
        """
        ...
