from src.domain.exceptions.base import AppException


class DatabaseError(AppException):
    message = "Произошла ошибка в базе данных"
    error_code = "DATABASE_ERROR"
    status_code = 500
