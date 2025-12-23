import pytest

from src.domain.entities.user import User
from src.domain.exceptions.validation import DomainValidationError


def test_create_user() -> None:
    user = User(
        tg_id=1,
        username="username",
        first_name="first_name",
        last_name="last_name",
        language_code="language_code",
    )
    assert user.tg_id == 1
    assert user.username == "username"
    assert user.first_name == "first_name"
    assert user.last_name == "last_name"
    assert user.language_code == "language_code"


def test_update_cached_balance() -> None:
    user = User(
        tg_id=1,
        username="username",
        first_name="first_name",
        last_name="last_name",
        language_code="language_code",
    )
    user.update_cached_balance(100)
    assert user.stars_balance == 100

    with pytest.raises(DomainValidationError):
        user.update_cached_balance(-1)

    user.update_cached_balance(0)
    assert user.stars_balance == 0


def test_set_admin() -> None:
    user = User(
        tg_id=1,
        username="username",
        first_name="first_name",
        last_name="last_name",
        language_code="language_code",
    )
    assert not user.is_admin
    user.set_admin()
    assert user.is_admin


def test_unset_admin() -> None:
    user = User(
        tg_id=1,
        username="username",
        first_name="first_name",
        last_name="last_name",
        language_code="language_code",
    )
    user.set_admin()
    assert user.is_admin
    user.unset_admin()
    assert not user.is_admin


def test_set_blocked() -> None:
    user = User(
        tg_id=1,
        username="username",
        first_name="first_name",
        last_name="last_name",
        language_code="language_code",
    )
    assert not user.is_blocked
    user.set_blocked()
    assert user.is_blocked


def test_set_unblocked() -> None:
    user = User(
        tg_id=1,
        username="username",
        first_name="first_name",
        last_name="last_name",
        language_code="language_code",
    )
    user.set_blocked()
    assert user.is_blocked
    user.set_unblocked()
    assert not user.is_blocked


