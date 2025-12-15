from typing import Protocol
from uuid import UUID

from src.domain.entities.game_round import GameRound


class BaseGameRoundRepository(Protocol):

    async def create(self, round: GameRound) -> None:
        """Создать игровой раунд."""

    async def get_by_bet_uuid(self, bet_uuid: UUID) -> GameRound | None:
        """Получить раунд по uuid ставки."""

    async def get_by_uuid(self, uuid: UUID) -> GameRound | None:
        """Получить раунд по uuid."""
