from abc import ABC, abstractmethod

from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode


class GamePayloadBuilder(ABC):
    @abstractmethod
    def supports(self, game_code: GameCode) -> bool:
        ...

    @abstractmethod
    def build(
        self,
        outcome_code: OutcomeCode,
        seed: str,
    ) -> dict:
        ...
