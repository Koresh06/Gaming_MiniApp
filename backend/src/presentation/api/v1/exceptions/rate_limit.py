from src.presentation.api.v1.exceptions.base import BaseHttpException


class RateLimitExceededException(BaseHttpException):
    message: str = "Превышен лимит запросов. Пожалуйста, попробуйте позже."
    error_code: str = "RATE_LIMIT_EXCEEDED"
    status_code: int = 429
