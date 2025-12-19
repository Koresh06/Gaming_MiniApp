from src.domain.exceptions.base import BaseInternalException


class DatabaseError(BaseInternalException):
    message = "Произошла ошибка в базе данных"
    error_code = "DATABASE_ERROR"
    status_code = 500
