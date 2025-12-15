from pydantic import BaseModel

from src.application.dtos.game_outcome_setting import GameOutcomeSettingInputDTO
from src.application.use_cases.game.get_outcome_settings import GetOutcomeSettingsRequest
from src.application.use_cases.game.update_outcome_settings import UpdateGameOutcomeSettingsRequest
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


class GetOutcomeSettingsSchema(BaseModel):
    game_code: GameCode

    def to_request(self) -> GetOutcomeSettingsRequest:
        return GetOutcomeSettingsRequest(game_code=self.game_code)


class UpdateOutcomeSettingItemSchema(BaseModel):
    outcome_code: OutcomeCode
    probability: float
    multiplier: float
    is_active: bool


class UpdateOutcomeSettingsSchema(BaseModel):
    settings: list[UpdateOutcomeSettingItemSchema]

    def to_request(self, game_code):

        dto_list = [
            GameOutcomeSettingInputDTO(
                game_code=game_code,
                outcome_code=item.outcome_code,
                probability=item.probability,
                multiplier=item.multiplier,
                is_active=item.is_active,
            )
            for item in self.settings
        ]

        return UpdateGameOutcomeSettingsRequest(game_code=game_code, settings=dto_list)