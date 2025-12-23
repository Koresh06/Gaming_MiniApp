from src.application.services.payload_builder.base import GamePayloadBuilder
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


class DartsPayloadBuilder(GamePayloadBuilder):
    def supports(self, game_code: GameCode) -> bool:
        return game_code == GameCode.DARTS

    def build(self, outcome_code: OutcomeCode, seed: str) -> dict:
        if outcome_code == OutcomeCode.LOSE:
            return {"hit": False}

        return {"hit": True}
