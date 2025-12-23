import pytest

from src.utils.uuid_v7 import uuid7
from src.domain.value_object.payout_status import PayoutStatus
from src.domain.entities.payout import Payout
from src.domain.exceptions.validation import DomainValidationError


@pytest.fixture
def sample_payout():
    return Payout(
        game_round_uuid=uuid7(),
        amount=100,
        status=PayoutStatus.PENDING,
        telegram_payout_id="telegram_payout_id",
    )


def test_create_payout(sample_payout: Payout):
    assert sample_payout.amount == 100
    assert sample_payout.status == PayoutStatus.PENDING
    assert sample_payout.telegram_payout_id == "telegram_payout_id"


def test_create_payout_with_zero_amount():
    with pytest.raises(DomainValidationError):
        Payout(
            game_round_uuid=uuid7(),
            amount=0,
            status=PayoutStatus.PENDING,
            telegram_payout_id="telegram_payout_id",
        )


def test_create_payout_with_negative_amount():
    with pytest.raises(DomainValidationError):
        Payout(
            game_round_uuid=uuid7(),
            amount=-100,
            status=PayoutStatus.PENDING,
            telegram_payout_id="telegram_payout_id",
        )