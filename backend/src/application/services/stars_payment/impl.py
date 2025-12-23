import aiohttp
import logging
from uuid import UUID

from src.domain.value_object.code_games import GameCode
from src.application.services.stars_payment.base import StarsPaymentServiceBase
from src.application.exceptions.stars import (
    StarsPaymentError,
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
        

    async def create_payment(self, amount: int, bet_uuid: UUID):
        logger.info(
            "Создание Stars Invoice",
            extra={"bet_uuid": str(bet_uuid)},
        )

        payload = {
            "title": "Game Bet",
            "description": "Game Bet payment",
            "payload": str(bet_uuid),

            "provider_token": "",
            "currency": "XTR",

            "prices": [
                {
                    "label": "Bet",
                    "amount": amount,
                }
            ],
        }

        invoice_link = await self._call_telegram_api(
            "createInvoiceLink",
            payload,
        )

        return invoice_link


    async def create_payout(self, tg_id: int, amount: int, round_uuid: UUID, game_code: GameCode) -> str:
        payload = {
            "chat_id": tg_id,
            "title": "Game Payout",
            "prices": [
                {
                    "label": "Payout",
                    "amount": amount,
                }
            ],
            "currency": "XTR",
            "payload": str(round_uuid),
            "description": f"Payout for {game_code}",
        }

        result = await self._call_telegram_api("sendInvoice", payload)

        logger.info(result)
        return str(result["message_id"])


    # async def process_payment_callback(self, bet_uuid: UUID, status: str, tx_id: str):
    #     logger.info("Обработка Stars payment callback", extra={
    #         "bet_uuid": str(bet_uuid),
    #         "status": status,
    #         "tx_id": tx_id
    #     })

    #     if not tx_id:
    #         raise StarsInvalidCallbackError("Отсутствует transaction_id")

    #     return True


    # async def process_payout_callback(self, payout_uuid: UUID, status: str, tx_id: str):
    #     logger.info("Обработка Stars payout callback", extra={
    #         "payout_uuid": str(payout_uuid),
    #         "status": status,
    #         "tx_id": tx_id
    #     })

    #     if not tx_id:
    #         raise StarsInvalidCallbackError("Отсутствует transaction_id")

    #     return True
