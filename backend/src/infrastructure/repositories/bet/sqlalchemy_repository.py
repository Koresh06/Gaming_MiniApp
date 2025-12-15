from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.bet import Bet
from src.infrastructure.database.models.bet import BetModel
from src.infrastructure.repositories.bet.base import BaseBetRepository   


class SQLAlchemyBetRepository(BaseBetRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, bet: Bet) -> None:
        bet_model = BetModel.from_entity(bet)
        self._session.add(bet_model)

    async def update(self, bet: Bet) -> None:
        stmt = select(BetModel).where(BetModel.uuid == bet.uuid)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise Exception("Bet not found")

        model.status = bet.status
        model.telegram_transaction_id = bet.telegram_transaction_id

        self._session.add(model)

    async def get_by_uuid(self, uuid: UUID) -> Bet | None:
        stmt = select(BetModel).where(BetModel.uuid == uuid)
        result = await self._session.execute(stmt)
        bet_model = result.scalar_one_or_none()
        return bet_model.to_entity() if bet_model else None
    
    async def get_for_user(self, user_uuid: UUID, limit: int = 50) -> list[Bet]:
        stmt = select(BetModel).where(BetModel.user_uuid == user_uuid).limit(limit)
        result = await self._session.execute(stmt)
        bet_models = result.scalars().all()
        return [bet_model.to_entity() for bet_model in bet_models]