from typing import Protocol
from uuid import UUID

from src.domain.entities.user import User


class BaseUserRepository(Protocol):
    async def create(self, user: User) -> None: ...

    async def get_by_uuid(self, user_uuid: UUID) -> User | None: ...

    async def get_by_tg_id(self, tg_id: int) -> User | None: ...