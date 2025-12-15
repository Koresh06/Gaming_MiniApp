from src.domain.exceptions.base import BaseInternalException


class StarsPaymentError(BaseInternalException):
    _status_code: int = 502
    _error_code: str = "STARS_PAYMENT_ERROR"
    _message: str = "Ошибка при создании платежа в Telegram Stars"


class StarsPayoutError(BaseInternalException):
    _status_code: int = 502
    _error_code: str = "STARS_PAYOUT_ERROR"
    _message: str = "Ошибка при выполнении выплаты Telegram Stars"


class StarsInvalidCallbackError(BaseInternalException):
    _status_code: int = 400
    _error_code: str = "STARS_INVALID_CALLBACK"
    _message: str = "Некорректный callback от Telegram"