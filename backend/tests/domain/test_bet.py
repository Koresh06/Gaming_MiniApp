import pytest

from src.utils.uuid_v7 import uuid7
from src.domain.entities.bet import Bet
from src.domain.value_object.bet_status import BetStatus
from src.domain.value_object.code_games import GameCode 
from src.domain.exceptions.validation import DomainValidationError


@pytest.fixture
def sample_bet():
    return Bet(user_uuid=uuid7(), game_code=GameCode.SLOT, amount=100)


def test_create_bet(sample_bet: Bet):
    assert sample_bet.game_code == GameCode.SLOT
    assert sample_bet.amount == 100

def test_create_bet_with_negative_amount():
    with pytest.raises(DomainValidationError):
        Bet(user_uuid=uuid7(), game_code=GameCode.SLOT, amount=-100)

def test_create_bet_with_zero_amount():
    with pytest.raises(DomainValidationError):
        Bet(user_uuid=uuid7(), game_code=GameCode.SLOT, amount=0)

def test_status_pending():
    bet = Bet(user_uuid=uuid7(), game_code=GameCode.SLOT, amount=100)
    assert bet.status == BetStatus.PENDING

def test_status_paid():
    bet = Bet(user_uuid=uuid7(), game_code=GameCode.SLOT, amount=100)
    bet.status = BetStatus.PAID
    assert bet.status == BetStatus.PAID

def test_status_failed():
    bet = Bet(user_uuid=uuid7(), game_code=GameCode.SLOT, amount=100)
    bet.status = BetStatus.FAILED
    assert bet.status == BetStatus.FAILED