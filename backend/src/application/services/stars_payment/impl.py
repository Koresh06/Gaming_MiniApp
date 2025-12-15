import aiohttp
import logging
from uuid import UUID

from src.application.services.stars_payment.base import StarsPaymentServiceBase
from src.application.exceptions.stars import (
    StarsPaymentError,
    StarsPayoutError,
    StarsInvalidCallbackError,
)

logger = logging.getLogger(__name__)


class ImplStarsPaymentService(StarsPaymentServiceBase):
    """
    Реальная интеграция с Telegram Stars API.
    """

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    async def _call_telegram_api(self, method: str, payload: dict) -> dict:
        """
        Унифицированный запрос к Telegram API.
        """
        url = f"{self.base_url}/{method}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    data = await resp.json()

                    if resp.status != 200 or not data.get("ok"):
                        logger.error("Ошибка Telegram API: %s", data)
                        raise ValueError(data)

                    return data["result"]

        except Exception as e:
            logger.exception("Ошибка HTTP запроса к Telegram API")
            raise StarsPaymentError(str(e))

    # ---------------------------------------------------------------------
    # 1. Создание инвойса Stars → Списание средств со ставки
    # ---------------------------------------------------------------------
    async def create_payment(self, tg_id: int, amount: int, bet_uuid: UUID) -> str:
        logger.info("Создание Stars Invoice", extra={"tg_id": tg_id, "bet_uuid": str(bet_uuid)})

        payload = {
            "user_id": tg_id,
            "amount": amount,
            "currency": "XTR",     # Важно!
            "payload": str(bet_uuid),
            "description": "Game Bet",
        }

        result = await self._call_telegram_api("createStarsInvoice", payload)
        return result["invoice_id"]

    # ---------------------------------------------------------------------
    # 2. Создание выплаты Stars → Выигрыш
    # ---------------------------------------------------------------------
    async def create_payout(self, tg_id: int, amount: int, round_uuid: UUID) -> str:
        logger.info("Создание Stars Withdrawal", extra={"tg_id": tg_id, "round_uuid": str(round_uuid)})

        payload = {
            "user_id": tg_id,
            "amount": amount,
            "currency": "XTR",
            "payload": str(round_uuid),
            "description": "Game Win",
        }

        result = await self._call_telegram_api("createStarsWithdrawal", payload)
        return result["withdrawal_id"]

    # ---------------------------------------------------------------------
    # 3. Обработка callback для платежей
    # ---------------------------------------------------------------------
    async def process_payment_callback(self, bet_uuid: UUID, status: str, tx_id: str):
        logger.info("Обработка Stars payment callback", extra={
            "bet_uuid": str(bet_uuid),
            "status": status,
            "tx_id": tx_id
        })

        if not tx_id:
            raise StarsInvalidCallbackError("Отсутствует transaction_id")

        # callback обработается в usecase UpdateBetStatusUseCase
        return True

    # ---------------------------------------------------------------------
    # 4. Обработка payout callback
    # ---------------------------------------------------------------------
    async def process_payout_callback(self, payout_uuid: UUID, status: str, tx_id: str):
        logger.info("Обработка Stars payout callback", extra={
            "payout_uuid": str(payout_uuid),
            "status": status,
            "tx_id": tx_id
        })

        if not tx_id:
            raise StarsInvalidCallbackError("Отсутствует transaction_id")

        return True
