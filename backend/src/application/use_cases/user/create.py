import logging
from dataclasses import dataclass

from src.domain.entities.user import User

from src.application.dtos.user import UserDTO
from src.application.use_cases.base import UseCaseRequest, UseCase

from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.user.base import BaseUserRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class CreateUserRequest(UseCaseRequest):
    tg_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str


@dataclass(frozen=True, eq=False)
class CreateUserUseCase(UseCase[CreateUserRequest, UserDTO]):
    user_repository: BaseUserRepository
    transaction_manager: TransactionManager

    async def __call__(self, request: CreateUserRequest) -> UserDTO:
        logger.info(
            "Создание нового пользователя",
            extra={
                "tg_id": request.tg_id,
                "username": request.username,
                "first_name": request.first_name,
                "last_name": request.last_name,
            }
        )

        user = User(
            tg_id=request.tg_id,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name,
            language_code=request.language_code,
            stars_balance=0,
        )

        try:
            await self.user_repository.create(user)
            await self.transaction_manager.commit()

        except Exception as e:
            logger.error(
                "Ошибка при создании пользователя",
                extra={
                    "tg_id": request.tg_id,
                    "exception": str(e),
                }
            )
            raise

        logger.info(
            "Пользователь успешно создан",
            extra={
                "user_uuid": str(user.uuid),
                "tg_id": user.tg_id,
                "username": user.username,
            }
        )

        return UserDTO.from_entity(user)