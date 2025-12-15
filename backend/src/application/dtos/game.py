from dataclasses import dataclass

from src.domain.entities.game import Game
from src.domain.value_object.code_games import GameCode


@dataclass(frozen=True, eq=False, kw_only=True)
class GameDTO:
    code: GameCode          
    name: str

    @classmethod
    def from_entity(cls, game: Game) -> "GameDTO":
        return GameDTO(
            code=game.code,
            name=game.name,
        )