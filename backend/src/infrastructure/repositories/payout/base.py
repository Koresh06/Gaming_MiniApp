from typing import Protocol
from uuid import UUID

from src.domain.entities.payout import Payout


class BasePayoutRepository(Protocol):

    async def create(self, payout: Payout) -> None:
        """Создать запись о выплате."""

    async def update(self, payout: Payout) -> None:
        """Обновить payout (статус и transaction id)."""

    async def get_by_game_round_uuid(self, round_uuid: UUID) -> Payout | None:
        """Получить выплату по uuid игрового раунда."""

    async def get_by_uuid(self, payout_id: UUID) -> Payout | None:
        """Получить выплату по uuid."""
