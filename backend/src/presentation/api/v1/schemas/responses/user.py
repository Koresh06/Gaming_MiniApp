from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from src.application.dtos.user import UserDTO


class UserResponseSchema(BaseModel):
    uuid: UUID
    tg_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: UserDTO) -> "UserResponseSchema":
        return cls(**dto.__dict__)



    
