from src.domain.exceptions.base import ApplicationException


class DomainValidationError(ApplicationException):
    status_code: int = 422
    error_code: str = "DOMAIN_VALIDATION_ERROR"
    message: str = "Произошла ошибка валидации"
