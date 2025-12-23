from src.application.services.payload_builder.base import GamePayloadBuilder
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


class FootballPayloadBuilder(GamePayloadBuilder):
    def supports(self, game_code: GameCode) -> bool:
        return game_code == GameCode.FOOTBALL

    def build(self, outcome_code: OutcomeCode, seed: str) -> dict:
        if outcome_code == OutcomeCode.LOSE:
            return {"goal": False}

        return {"goal": True}