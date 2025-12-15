from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.game_round import GameRound
from src.infrastructure.database.models.game_round import GameRoundModel
from src.infrastructure.repositories.game_round.base import BaseGameRoundRepository 


class SQLAlchemyGameRoundRepository(BaseGameRoundRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, round: GameRound) -> None:
        round_model = GameRoundModel.from_entity(round)
        self._session.add(round_model)

    async def get_by_uuid(self, uuid: UUID) -> GameRound | None:
        query = select(GameRoundModel).where(GameRoundModel.uuid == uuid)
        result = await self._session.execute(query)
        game_round_model = result.scalars().one_or_none()
        return game_round_model.to_entity()

    async def get_by_bet_uuid(self, bet_uuid: UUID) -> GameRound | None:
        query = select(GameRoundModel).where(GameRoundModel.bet_uuid == bet_uuid)
        result = await self._session.execute(query)
        game_round_model = result.scalars().one_or_none()
        return game_round_model.to_entity()

    