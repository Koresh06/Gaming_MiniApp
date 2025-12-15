from typing import Protocol

from src.domain.entities.game_outcome_setting import GameOutcomeSetting
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


class BaseGameOutcomeSettingRepository(Protocol):

    async def get_active_for_game(self, game_code: GameCode) -> list[GameOutcomeSetting]:
        ...

    async def get_all_for_game(self, game_code: GameCode) -> list[GameOutcomeSetting]:
        ...

    async def update_settings(self, game_code: GameCode, settings: list[GameOutcomeSetting]) -> None:
        ...

    async def get(self, game_code: GameCode, outcome_code: OutcomeCode) -> GameOutcomeSetting | None:
        ...
