from src.domain.exceptions.base import ApplicationException


class StarsPaymentError(ApplicationException):
    status_code: int = 502
    error_code: str = "STARS_PAYMENT_ERROR"
    message: str = "Ошибка при создании платежа в Telegram Stars"


class StarsPayoutError(ApplicationException):
    status_code: int = 502
    error_code: str = "STARS_PAYOUT_ERROR"
    message: str = "Ошибка при выполнении выплаты Telegram Stars"


class StarsInvalidCallbackError(ApplicationException):
    status_code: int = 400
    error_code: str = "STARS_INVALID_CALLBACK"
    message: str = "Некорректный callback от Telegram"
