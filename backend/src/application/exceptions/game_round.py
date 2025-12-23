from src.application.exceptions.base import LogicException


class GameRoundNotFound(LogicException):
    status_code: int = 404
    error_code: str = "GAME_ROUND_NOT_FOUND"
    message: str = "Раунд игры не найден"
