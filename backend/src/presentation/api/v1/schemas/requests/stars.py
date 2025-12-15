from pydantic import BaseModel, Field
from uuid import UUID

from src.application.use_cases.bet.update import UpdateBetStatusRequest
from src.application.use_cases.payout.update import UpdatePayoutStatusRequest
from src.domain.value_object.bet_status import BetStatus
from src.domain.value_object.payout_status import PayoutStatus


class StarsPaymentCallbackSchema(BaseModel):
    bet_uuid: UUID = Field(..., description="UUID ставки")
    status: str = Field(..., description="Статус оплаты: paid / failed")
    telegram_transaction_id: str | None = Field(None, description="ID транзакции Stars")
    
    def to_request(self) -> UpdateBetStatusRequest:
        return UpdateBetStatusRequest(
            bet_uuid=self.bet_uuid,
            status=BetStatus.PAID if self.status == "paid" else BetStatus.FAILED,
            telegram_transaction_id=self.telegram_transaction_id,
        )

class StarsPayoutCallbackSchema(BaseModel):
    payout_uuid: UUID
    status: PayoutStatus
    telegram_transaction_id: str | None

    def to_request(self) -> UpdatePayoutStatusRequest:
        return UpdatePayoutStatusRequest(
            payout_uuid=self.payout_uuid,
            status=self.status,
            telegram_payout_id=self.telegram_transaction_id,
        )
