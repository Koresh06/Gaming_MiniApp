from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.repositories.user.base import BaseUserRepository    


class SQLAlchemyUserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user: User) -> None:
        user_model = UserModel.from_entity(user)
        self._session.add(user_model)

    async def get_by_uuid(self, user_uuid: UUID) -> User | None:
        query = select(UserModel).where(UserModel.uuid == user_uuid)
        result = await self._session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None
    
    async def get_by_tg_id(self, tg_id: int) -> User | None:
        query = select(UserModel).where(UserModel.tg_id == tg_id)
        result = await self._session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None