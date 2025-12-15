from dataclasses import dataclass

from .base import Entity
from src.domain.exceptions.validation import DomainValidationError


@dataclass(kw_only=True)
class User(Entity):
    tg_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str
    stars_balance: int = 0       
    is_admin: bool = False
    is_blocked: bool = False

    def update_cached_balance(self, balance: int):
        if balance < 0:
            raise DomainValidationError(message="Баланс должен быть неотрицательным.")
        self.stars_balance = balance

    def set_admin(self):
        self.is_admin = True

    def unset_admin(self):
        self.is_admin = False

    def set_blocked(self):
        self.is_blocked = True

    def set_unblocked(self):
        self.is_blocked = False

    