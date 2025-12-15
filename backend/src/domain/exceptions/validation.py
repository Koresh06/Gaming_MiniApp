from src.domain.exceptions.base import BaseInternalException


class DomainValidationError(BaseInternalException):
    _status_code: int = 422
    _error_code: str = "DOMAIN_VALIDATION_ERROR"
    _message: str = "Произошла ошибка валидации"
