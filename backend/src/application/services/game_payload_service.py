from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode
from src.application.services.payload_builder.base import GamePayloadBuilder



class GamePayloadService:
    def __init__(self, builders: list[GamePayloadBuilder]):
        self._builders = builders

    def build_payload(
        self,
        game_code: GameCode,
        outcome_code: OutcomeCode,
        seed: str,
    ) -> dict:
        for builder in self._builders:
            if builder.supports(game_code):
                return builder.build(outcome_code, seed)

        raise ValueError(f"No payload builder for game {game_code}")
