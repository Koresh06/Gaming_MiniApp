import pytest

from src.utils.uuid_v7 import uuid7
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode
from src.domain.entities.game_round import GameRound
from src.domain.exceptions.validation import DomainValidationError


@pytest.fixture
def sample_game_round():
    return GameRound(
        bet_uuid=uuid7(),
        user_uuid=uuid7(),
        game_code=GameCode.SLOT,
        outcome_code=OutcomeCode.WIN,
        is_win=True,
        win_amount=100,
        seed="seed",
    )


def test_create_game_round(sample_game_round: GameRound):
    assert sample_game_round.game_code == GameCode.SLOT
    assert sample_game_round.outcome_code == OutcomeCode.WIN
    assert sample_game_round.is_win
    assert sample_game_round.win_amount == 100

def test_invalid_win_amount():
    with pytest.raises(DomainValidationError):
        GameRound(
            bet_uuid=uuid7(),
            user_uuid=uuid7(),
            game_code=GameCode.SLOT,
            outcome_code=OutcomeCode.WIN,
            is_win=True,
            win_amount=-100,
            seed="seed",
        )

def test_invalid_seed():
    with pytest.raises(DomainValidationError):
        GameRound(
            bet_uuid=uuid7(),
            user_uuid=uuid7(),
            game_code=GameCode.SLOT,
            outcome_code=OutcomeCode.WIN,
            is_win=True,
            win_amount=100,
            seed="",
        )