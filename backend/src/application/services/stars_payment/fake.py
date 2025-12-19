import logging
from uuid import UUID

from src.application.exceptions.stars import StarsInvalidCallbackError
from src.application.services.stars_payment.base import StarsPaymentServiceBase


logger = logging.getLogger(__name__)


class FakeStarsPaymentService(StarsPaymentServiceBase):
    """
    Фейковая реализация Stars API.
    Используется для разработки и локальных тестов.
    """

    async def create_payment(self, amount: int, bet_uuid: UUID) -> str:
        logger.info(
            "[FAKE STARS] Создание платежа",
            extra={"amount": amount, "bet_uuid": str(bet_uuid)}
        )

        return f"fake_invoice_{bet_uuid}"

    async def create_payout(self, tg_id: int, amount: int, round_uuid: UUID) -> str:
        logger.info(
            "[FAKE STARS] Создание выплаты",
            extra={"tg_id": tg_id, "amount": amount, "round_uuid": str(round_uuid)}
        )

        return f"fake_payout_{round_uuid}"

    # async def process_payment_callback(self, bet_uuid: UUID, status: str, tx_id: str):
    #     logger.info(
    #         "[FAKE STARS] callback payment",
    #         extra={"bet_uuid": str(bet_uuid), "status": status, "tx_id": tx_id}
    #     )

    #     if not tx_id:
    #         raise StarsInvalidCallbackError("FAKE: отсутствует transaction_id")

    # async def process_payout_callback(self, payout_uuid: UUID, status: str, tx_id: str):
    #     logger.info(
    #         "[FAKE STARS] callback payout",
    #         extra={"payout_uuid": str(payout_uuid), "status": status, "tx_id": tx_id}
    #     )

    #     if not tx_id:
    #         raise StarsInvalidCallbackError("FAKE: отсутствует transaction_id")
