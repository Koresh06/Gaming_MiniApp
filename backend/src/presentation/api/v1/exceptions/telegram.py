from src.presentation.api.v1.exceptions.base import BaseHttpException


class InvalidTelegramSignature(BaseHttpException):
    _status_code = 403
    _error_code = "INVALID_STARS_SIGNATURE"
    _message = "Invalid Telegram Stars signature"


class MissingTelegramSignature(BaseHttpException):
    _status_code = 401
    _error_code = "MISSING_STARS_SIGNATURE"
    _message = "Missing Telegram Stars signature"
