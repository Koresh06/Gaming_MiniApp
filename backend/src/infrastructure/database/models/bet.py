from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Enum as SaEnum, ForeignKey, Integer, String

from src.domain.entities.bet import Bet
from src.domain.value_object.bet_status import BetStatus
from src.domain.value_object.code_games import GameCode
from src.infrastructure.database.models.base import (
    BaseModel,
    CreatedAtMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from src.infrastructure.database.models import UserModel, GameRoundModel


class BetModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "bets"

    uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        unique=True,
    )
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    game_code: Mapped[GameCode] = mapped_column(SaEnum(GameCode))
    amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[BetStatus] = mapped_column(SaEnum(BetStatus))
    telegram_transaction_id: Mapped[str | None] = mapped_column(String, nullable=True)

    user_rel: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="bet_rel",
    )
    game_round_rel: Mapped["GameRoundModel"] = relationship(
        "GameRoundModel", 
        back_populates="bet_rel", 
        uselist=False,
    )

    def to_entity(self) -> Bet:
        return Bet(
            uuid=self.uuid,
            user_uuid=self.user_uuid,
            game_code=self.game_code,
            amount=self.amount,
            status=BetStatus(self.status),
            telegram_transaction_id=self.telegram_transaction_id,
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(entity: Bet) -> "BetModel":
        return BetModel(
            uuid=entity.uuid,
            user_uuid=entity.user_uuid,
            game_code=entity.game_code,
            amount=entity.amount,
            status=entity.status.value,
            telegram_transaction_id=entity.telegram_transaction_id,
        )
