from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from src.application.dtos.bet import BetDTO
from src.application.dtos.payment import InitPaymentDTO


class BetResponseSchema(BaseModel):
    uuid: UUID
    user_uuid: UUID
    game_code: str
    amount: int
    status: str
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: BetDTO) -> "BetResponseSchema":
        return cls(**dto.__dict__)


class InitPaymentResponseSchema(BaseModel):
    invoice_id: str

    @classmethod
    def from_dto(cls, dto: InitPaymentDTO) -> "InitPaymentResponseSchema":
        return cls(**dto.__dict__)
