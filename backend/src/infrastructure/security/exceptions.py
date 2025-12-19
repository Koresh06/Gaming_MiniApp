from src.domain.exceptions.base import BaseInternalException


class TelegramAuthError(BaseInternalException):
    message = "Неверные данные инициализации Telegram."
    error_code = "TELEGRAM_AUTH_ERROR"
    status_code = 401
