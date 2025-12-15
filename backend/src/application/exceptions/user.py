from src.application.exceptions.base import LogicException


class UserNotFound(LogicException):
    _status_code: int = 404
    _error_code: str = "USER_NOT_FOUND"
    _message: str = "Пользователь не найден"


class ForbiddenAccess(LogicException):
    _error_code: str = "FORBIDDEN"
    _status_code: int = 403
    _message: str = "Недостаточно прав"
