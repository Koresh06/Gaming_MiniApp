from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Integer, String, BigInteger

from src.domain.entities.user import User
from src.infrastructure.database.models.base import (
    BaseModel,
    CreatedAtMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from src.infrastructure.database.models import BetModel, GameRoundModel


class UserModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        unique=True,
    )
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String)
    language_code: Mapped[str] = mapped_column(String)

    stars_balance: Mapped[int] = mapped_column(Integer, default=0)
    is_admin: Mapped[bool] = mapped_column(Integer, default=False)
    is_blocked: Mapped[bool] = mapped_column(Integer, default=False)

    game_round_rel: Mapped[list["GameRoundModel"]] = relationship(
        "GameRoundModel",
        back_populates="user_rel",
    )
    bet_rel: Mapped["BetModel"] = relationship(
        "BetModel",
        back_populates="user_rel",
    )

    @classmethod
    def from_entity(cls, user: "User") -> "UserModel":
        return cls(
            uuid=user.uuid,
            tg_id=user.tg_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code,
            stars_balance=user.stars_balance,
            is_admin=user.is_admin,
            is_blocked=user.is_blocked,
        )

    def to_entity(self) -> "User":
        return User(
            uuid=self.uuid,
            tg_id=self.tg_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            language_code=self.language_code,
            stars_balance=self.stars_balance,
            is_admin=self.is_admin,
            is_blocked=self.is_blocked,
        )
