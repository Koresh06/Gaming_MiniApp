from typing import Protocol
from uuid import UUID

from src.domain.entities.bet import Bet


class BaseBetRepository(Protocol):

    async def create(self, bet: Bet) -> None:
        """Создать ставку со статусом PENDING."""

    async def update(self, bet: Bet) -> None:
        """Обновить ставку (статус, транзакция...)."""

    async def get_by_uuid(self, uuid: UUID) -> Bet | None:
        """Получить ставку по её uuid."""

    async def get_for_user(self, user_uuid: UUID, limit: int = 50) -> list[Bet]:
        """Получить историю ставок пользователя."""
