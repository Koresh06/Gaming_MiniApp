from src.application.exceptions.base import LogicException


class PayoutNotFound(LogicException):
    _status_code: int = 404
    _error_code: str = "PAYOUT_NOT_FOUND"
    _message: str = "Платеж не найден"