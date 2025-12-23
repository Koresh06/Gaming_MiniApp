import random

from src.application.services.payload_builder.base import GamePayloadBuilder
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


class DicePayloadBuilder(GamePayloadBuilder):
    def supports(self, game_code: GameCode) -> bool:
        return game_code == GameCode.DICE

    def build(self, outcome_code: OutcomeCode, seed: str) -> dict:
        rnd = random.Random(seed)

        if outcome_code == OutcomeCode.LOSE:
            return {"dice": rnd.randint(1, 5)}

        return {"dice": 6}
