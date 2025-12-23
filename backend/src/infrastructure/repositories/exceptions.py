from src.domain.exceptions.base import ApplicationException


class DatabaseError(ApplicationException):
    message = "Произошла ошибка в базе данных"
    error_code = "DATABASE_ERROR"
    status_code = 500
