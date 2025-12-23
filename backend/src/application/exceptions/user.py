from src.application.exceptions.base import LogicException


class UserNotFound(LogicException):
    status_code: int = 404
    error_code: str = "USER_NOT_FOUND"
    message: str = "Пользователь не найден"


class ForbiddenAccess(LogicException):
    status_code: int = 403
    error_code: str = "FORBIDDEN"
    message: str = "Недостаточно прав"
