from src.presentation.api.v1.exceptions.base import BaseHttpException


class RateLimitExceededException(BaseHttpException):
    _message: str = "Превышен лимит запросов. Пожалуйста, попробуйте позже."
    _error_code: str = "RATE_LIMIT_EXCEEDED"
    _status_code: int = 429