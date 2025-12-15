from dataclasses import dataclass

from src.domain.value_object.code_games import GameCode


@dataclass(kw_only=True)
class Game:
    code: GameCode          
    name: str