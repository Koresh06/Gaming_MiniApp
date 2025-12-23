from src.application.exceptions.base import LogicException


class PayoutNotFound(LogicException):
    status_code: int = 404
    error_code: str = "PAYOUT_NOT_FOUND"
    message: str = "Платеж не найден"
