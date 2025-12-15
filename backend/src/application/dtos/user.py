from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.entities.user import User


@dataclass(frozen=True, eq=False, kw_only=True)
class UserDTO:
    uuid: UUID
    tg_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str
    stars_balance: int     
    is_admin: bool
    is_blocked: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "UserDTO":
        return UserDTO(
            uuid=user.uuid,
            tg_id=user.tg_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name, 
            language_code=user.language_code,
            stars_balance=user.stars_balance,
            is_admin=user.is_admin,
            is_blocked=user.is_blocked,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )