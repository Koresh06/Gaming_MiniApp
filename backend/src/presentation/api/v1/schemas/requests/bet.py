from uuid import UUID
from pydantic import BaseModel

from src.application.use_cases.bet.create import CreateBetRequest
from src.application.use_cases.payment.init import InitPaymentRequest
from src.domain.value_object.code_games import GameCode


class CreateBetSchema(BaseModel):
    user_uuid: UUID
    game_code: GameCode
    amount: int

    def to_request(self) -> CreateBetRequest:
        return CreateBetRequest(
            user_uuid=self.user_uuid,
            game_code=self.game_code,
            amount=self.amount,
        )


class InitPaymentSchema(BaseModel):
    bet_uuid: UUID

    def to_request(self) -> InitPaymentRequest:
        return InitPaymentRequest(bet_uuid=self.bet_uuid)
