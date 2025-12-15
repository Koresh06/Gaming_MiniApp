from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Enum as SaEnum, ForeignKey, Boolean, Integer, String

from src.domain.entities.game_round import GameRound
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode
from src.infrastructure.database.models.base import (
    BaseModel,
    CreatedAtMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from src.infrastructure.database.models import UserModel, BetModel, PayoutModel


class GameRoundModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "game_rounds"

    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    bet_uuid: Mapped[UUID] = mapped_column(ForeignKey("bets.uuid"), unique=True)
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))
    game_code: Mapped[GameCode] = mapped_column(SaEnum(GameCode))
    outcome_code: Mapped[OutcomeCode] = mapped_column(SaEnum(OutcomeCode))
    is_win: Mapped[bool] = mapped_column(Boolean)
    win_amount: Mapped[int] = mapped_column(Integer)
    seed: Mapped[str] = mapped_column(String)

    user_rel: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="game_round_rel",
    )
    bet_rel: Mapped["BetModel"] = relationship(
        "BetModel",
        back_populates="game_round_rel",
    )
    payout_rel: Mapped["PayoutModel"] = relationship(
        "PayoutModel",
        back_populates="game_round_rel",
        uselist=False,
    )

    def to_entity(self) -> GameRound:
        return GameRound(
            uuid=self.uuid,
            bet_uuid=self.bet_uuid,
            user_uuid=self.user_uuid,
            game_code=self.game_code,
            outcome_code=OutcomeCode(self.outcome_code),
            is_win=self.is_win,
            win_amount=self.win_amount,
            seed=self.seed,
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(entity: GameRound) -> "GameRoundModel":
        return GameRoundModel(
            uuid=entity.uuid,
            bet_uuid=entity.bet_uuid,
            user_uuid=entity.user_uuid,
            game_code=entity.game_code,
            outcome_code=entity.outcome_code.value,
            is_win=entity.is_win,
            win_amount=entity.win_amount,
            seed=entity.seed,
        )
