from src.application.exceptions.base import LogicException


class BetNotFound(LogicException):
    status_code: int = 404
    error_code: str = "BET_NOT_FOUND"
    message: str = "Ставка не найдена"


class BetNotPaid(LogicException):
    status_code: int = 400
    error_code: str = "BET_NOT_PAID"
    message: str = "Ставка не оплачена"


class BetAlreadyPaid(LogicException):
    status_code: int = 400
    error_code: str = "BET_ALREADY_PAID"
    message: str = "Ставка уже оплачена"
