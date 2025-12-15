from src.application.exceptions.base import LogicException


class BetNotFound(LogicException):
    _status_code: int =  404
    _error_code: str = "BET_NOT_FOUND"
    _message: str = "Ставка не найдена"


class BetNotPaid(LogicException):
    _status_code: int = 400
    _error_code: str = "BET_NOT_PAID"
    _message: str = "Ставка не оплачена"