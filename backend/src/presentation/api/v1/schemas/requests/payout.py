from uuid import UUID
from pydantic import BaseModel

from src.application.use_cases.payout.process import ProcessPayoutRequest


class ProcessPayoutSchema(BaseModel):
    game_round_uuid: UUID

    def to_request(self) -> ProcessPayoutRequest:
        return ProcessPayoutRequest(game_round_uuid=self.game_round_uuid)
