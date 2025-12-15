from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.payout import Payout
from src.infrastructure.database.models.payout import PayoutModel
from src.infrastructure.repositories.payout.base import BasePayoutRepository


class SQLAlchemyPayoutRepository(BasePayoutRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, payout: Payout) -> None:
        payout_model = PayoutModel.from_entity(payout)
        self._session.add(payout_model)

    async def get_by_uuid(self, payout_id: UUID) -> Payout | None:
        query = select(PayoutModel).where(PayoutModel.uuid == payout_id)
        result = await self._session.execute(query)
        payout_model = result.scalars().one_or_none()
        return payout_model.to_entity()

    async def update(self, payout: Payout) -> None:
        stmt = select(PayoutModel).where(PayoutModel.uuid == payout.uuid)
        result = await self._session.execute(stmt)
        payout_model = result.scalar_one_or_none()

        if payout_model is None:
            raise Exception("Payout not found")

        payout_model.status = payout.status
        payout_model.telegram_payout_id = payout.telegram_payout_id

        self._session.add(payout_model)

    async def get_by_game_round_uuid(self, round_uuid: UUID) -> Payout | None:
        query = select(PayoutModel).where(PayoutModel.game_round_uuid == round_uuid)
        result = await self._session.execute(query)
        payout_model = result.scalars().one_or_none()
        return payout_model.to_entity()