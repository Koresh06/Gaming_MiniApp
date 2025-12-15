from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Enum as SaEnum

from src.domain.entities.game_outcome_setting import GameOutcomeSetting
from src.domain.value_object.code_games import GameCode
from src.domain.value_object.outcome_code import OutcomeCode
from src.infrastructure.database.models.base import (
    BaseModel,
    CreatedAtMixin,
    UpdatedAtMixin,
)


class GameOutcomeSettingModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "game_outcome_settings"

    uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        unique=True,
    )
    game_code: Mapped[GameCode] = mapped_column(SaEnum(GameCode))
    outcome_code: Mapped[OutcomeCode] = mapped_column(SaEnum(OutcomeCode))
    probability: Mapped[float] = mapped_column(default=0.0)
    multiplier: Mapped[float] = mapped_column(default=0.0)
    is_active: Mapped[bool] = mapped_column(default=True)


    @staticmethod
    def from_entity(entity: GameOutcomeSetting) -> "GameOutcomeSettingModel":
        return GameOutcomeSettingModel(
            uuid=entity.uuid,
            game_code=entity.game_code,
            outcome_code=entity.outcome_code.value,
            probability=entity.probability,
            multiplier=entity.multiplier,
            is_active=entity.is_active,
        )
    
    def to_entity(self) -> GameOutcomeSetting:
        return GameOutcomeSetting(
            uuid=self.uuid,
            game_code=self.game_code,
            outcome_code=OutcomeCode(self.outcome_code),
            probability=self.probability,
            multiplier=self.multiplier,
            is_active=self.is_active,
        )

