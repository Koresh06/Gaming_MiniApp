from src.presentation.api.v1.exceptions.base import BaseHttpException


class InvalidTelegramSignature(BaseHttpException):
    status_code = 403
    error_code = "INVALID_STARS_SIGNATURE"
    message = "Invalid Telegram Stars signature"


class MissingTelegramSignature(BaseHttpException):
    status_code = 401
    error_code = "MISSING_STARS_SIGNATURE"
    message = "Missing Telegram Stars signature"
