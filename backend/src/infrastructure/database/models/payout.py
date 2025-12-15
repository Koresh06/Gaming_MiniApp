from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Enum as SaEnum, ForeignKey, Integer, String

from src.domain.entities.payout import Payout
from src.domain.value_object.payout_status import PayoutStatus
from src.infrastructure.database.models.base import (
    BaseModel,
    CreatedAtMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from src.infrastructure.database.models import GameRoundModel


class PayoutModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "payouts"

    uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        unique=True,
    )
    game_round_uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("game_rounds.uuid"),
        unique=True
    )
    amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[PayoutStatus] = mapped_column(SaEnum(PayoutStatus))
    telegram_payout_id: Mapped[str | None] = mapped_column(String, nullable=True)

    game_round_rel: Mapped["GameRoundModel"] = relationship(
        "GameRoundModel",
        back_populates="payout_rel"
    )

    @staticmethod
    def from_entity(entity: Payout) -> "PayoutModel":
        return PayoutModel(
            uuid=entity.uuid,
            game_round_uuid=entity.game_round_uuid,
            amount=entity.amount,
            status=entity.status.value,
            telegram_payout_id=entity.telegram_payout_id,
        )
    
    def to_entity(self) -> Payout:
        return Payout(
            uuid=self.uuid,
            game_round_uuid=self.game_round_uuid,
            amount=self.amount,
            status=PayoutStatus(self.status),
            telegram_payout_id=self.telegram_payout_id,
            created_at=self.created_at,
        )

