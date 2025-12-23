from src.domain.exceptions.base import ApplicationException


class TelegramAuthError(ApplicationException):
    message = "Неверные данные инициализации Telegram."
    error_code = "TELEGRAM_AUTH_ERROR"
    status_code = 401
