from pydantic import BaseModel

from src.application.use_cases.user.create import CreateUserRequest


class CreateUserSchema(BaseModel):
    tg_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str

    def to_request(self) -> CreateUserRequest:
        return CreateUserRequest(
            tg_id=self.tg_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            language_code=self.language_code,
        )