
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.game_outcome_setting import GameOutcomeSetting
from src.domain.value_object.code_games import GameCode
from src.infrastructure.database.models.game_outcome_settings import (
    GameOutcomeSettingModel,
)
from src.infrastructure.repositories.game_outcome_settings.base import (
    BaseGameOutcomeSettingRepository,
)


class SQLAlchemyGameOutcomeSettingRepository(BaseGameOutcomeSettingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_for_game(self, game_code: GameCode) -> list[GameOutcomeSetting]:
        query = select(GameOutcomeSettingModel).where(
            GameOutcomeSettingModel.game_code == game_code
        )
        result = await self._session.execute(query)
        game_outcome_settings: list[GameOutcomeSettingModel] = list(
            result.scalars().all()
        )
        return [
            game_outcome_setting.to_entity()
            for game_outcome_setting in game_outcome_settings
        ]

    async def get_active_for_game(self, game_code: GameCode) -> list[GameOutcomeSetting]:
        query = select(GameOutcomeSettingModel).where(
            GameOutcomeSettingModel.game_code == game_code,
            GameOutcomeSettingModel.is_active == True,
        )
        result = await self._session.execute(query)
        game_outcome_settings: list[GameOutcomeSettingModel] = list(
            result.scalars().all()
        )
        return [
            game_outcome_setting.to_entity()
            for game_outcome_setting in game_outcome_settings
        ]

    async def update_settings(
        self,
        game_code: GameCode,
        settings: list[GameOutcomeSetting],
    ) -> None:
        query = select(GameOutcomeSettingModel).where(
            GameOutcomeSettingModel.game_code == game_code
        )
        result = await self._session.execute(query)
        game_outcome_settings: list[GameOutcomeSettingModel] = list(
            result.scalars().all()
        )
        for game_outcome_setting in game_outcome_settings:
            await self._session.delete(game_outcome_setting)
        for setting in settings:
            self._session.add(GameOutcomeSettingModel.from_entity(setting))
        await self._session.commit()

    async def get(
        self,
        game_code: GameCode,
        outcome_code: str,
    ) -> GameOutcomeSetting | None:
        query = select(GameOutcomeSettingModel).where(
            GameOutcomeSettingModel.game_code == game_code,
            GameOutcomeSettingModel.outcome_code == outcome_code,
        )
        result = await self._session.execute(query)
        game_outcome_setting = result.scalar_one_or_none()
        return game_outcome_setting.to_entity() if game_outcome_setting else None
