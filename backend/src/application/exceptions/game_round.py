from src.application.exceptions.base import LogicException


class GameRoundNotFound(LogicException):
    _status_code: int = 404
    _error_code: str = "GAME_ROUND_NOT_FOUND"
    _message: str = "Раунд игры не найден"