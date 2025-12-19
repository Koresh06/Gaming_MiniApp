from dataclasses import dataclass

from src.application.dtos.auth import AuthResultDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.application.use_cases.user.get_by_tg_id import GetUserByTgIdRequest, GetUserByTgIdUseCase
from src.application.use_cases.user.create import CreateUserRequest, CreateUserUseCase
from src.infrastructure.security.exceptions import TelegramAuthError
from src.infrastructure.security.auth import verify_telegram_init_data
from src.infrastructure.security.jwt import JWTService


@dataclass(frozen=True)
class TelegramAuthRequest(UseCaseRequest):
    init_data: str


@dataclass(frozen=True)
class TelegramAuthUseCase(UseCase[TelegramAuthRequest, AuthResultDTO]):
    bot_token: str
    jwt_service: JWTService
    get_user_by_tg_id_use_case: GetUserByTgIdUseCase
    create_user_use_case: CreateUserUseCase

    async def __call__(self, request: TelegramAuthRequest) -> AuthResultDTO:
        try:
            data = verify_telegram_init_data(request.init_data, self.bot_token)
        except TelegramAuthError:
            raise
            
        tg_user = data["user"]
        tg_id = tg_user["id"]

        user = await self.get_user_by_tg_id_use_case(GetUserByTgIdRequest(tg_id=tg_id))

        if not user:
            user = await self.create_user_use_case(
                CreateUserRequest(
                    tg_id=tg_id,
                    username=tg_user.get("username"),
                    first_name=tg_user.get("first_name"),
                    last_name=tg_user.get("last_name"),
                    language_code=tg_user.get("language_code", "en"),
                )
            )

        token = self.jwt_service.create_token(subject=str(user.tg_id))

        return AuthResultDTO(access_token=token)
