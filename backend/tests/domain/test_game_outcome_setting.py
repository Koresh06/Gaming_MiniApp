import pytest

from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode
from src.domain.entities.game_outcome_setting import GameOutcomeSetting
from src.domain.exceptions.validation import DomainValidationError


@pytest.fixture
def sample_game_outcome_setting():
    return GameOutcomeSetting(
        game_code=GameCode.SLOT,
        outcome_code=OutcomeCode.WIN,
        probability=0.5,
        multiplier=2.0,
        is_active=True
    )

def test_create_game_outcome_setting(sample_game_outcome_setting: GameOutcomeSetting):
    assert sample_game_outcome_setting.game_code == GameCode.SLOT
    assert sample_game_outcome_setting.outcome_code == OutcomeCode.WIN
    assert sample_game_outcome_setting.probability == 0.5
    assert sample_game_outcome_setting.multiplier == 2.0
    assert sample_game_outcome_setting.is_active

def test_invalid_multiplier():
    with pytest.raises(DomainValidationError):
        GameOutcomeSetting(
            game_code=GameCode.SLOT,
            outcome_code=OutcomeCode.WIN,
            probability=0.5,
            multiplier=-2.0,
            is_active=True
        )

def test_invalid_probability():
    with pytest.raises(DomainValidationError):
        GameOutcomeSetting(
            game_code=GameCode.SLOT,
            outcome_code=OutcomeCode.WIN,
            probability=-0.5,
            multiplier=2.0,
            is_active=True
        )

    with pytest.raises(DomainValidationError):
        GameOutcomeSetting(
            game_code=GameCode.SLOT,
            outcome_code=OutcomeCode.WIN,
            probability=1.5,
            multiplier=2.0,
            is_active=True
        )