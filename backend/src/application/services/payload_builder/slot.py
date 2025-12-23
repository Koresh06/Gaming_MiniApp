from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode
from src.application.services.payload_builder.base import GamePayloadBuilder


class SlotPayloadBuilder(GamePayloadBuilder):
    def supports(self, game_code: GameCode) -> bool:
        return game_code == GameCode.SLOT

    def build(self, outcome_code: OutcomeCode, seed: str) -> dict:
        if outcome_code == OutcomeCode.JACKPOT:
            return {
                "slot": {
                    "pattern": "jackpot"
                }
            }

        if outcome_code == OutcomeCode.WIN:
            return {
                "slot": {
                    "pattern": "win"
                }
            }

        return {
            "slot": {
                "pattern": "lose"
            }
        }
