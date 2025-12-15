import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.presentation.api.v1.exceptions.telegram import InvalidTelegramSignature, MissingTelegramSignature


logger = logging.getLogger(__name__)


STARS_CALLBACK_PATHS = {
    "/stars/payment/callback",
    "/stars/payout/callback",
}


class TelegramSignatureMiddleware(BaseHTTPMiddleware):
    """
    Проверка заголовка X-Telegram-Bot-Api-Secret-Token для Stars callback.
    """

    def __init__(self, app, secret_token: str):
        super().__init__(app)
        self.secret_token = secret_token

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Проверяем только нужные endpoints
        if path in STARS_CALLBACK_PATHS:
            received_signature = request.headers.get("X-Telegram-Bot-Api-Secret-Token")

            if not received_signature:
                logger.warning("Stars callback пришёл БЕЗ сигнатуры", extra={"path": path})
                return MissingTelegramSignature.get_response()

            if received_signature != self.secret_token:
                logger.warning(
                    "Stars callback с НЕВЕРНОЙ сигнатурой",
                    extra={"path": path, "received": received_signature},
                )
                return InvalidTelegramSignature.get_response()

            logger.info("Stars signature OK", extra={"path": path})

        return await call_next(request)
