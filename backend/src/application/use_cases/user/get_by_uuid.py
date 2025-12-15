import logging
from uuid import UUID
from dataclasses import dataclass

from src.application.exceptions.user import UserNotFound
from src.application.dtos.user import UserDTO
from src.application.use_cases.base import UseCaseRequest, UseCase

from src.infrastructure.repositories.user.base import BaseUserRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class GetUserByUUIDRequest(UseCaseRequest):
    user_uuid: UUID
    # current_user_uuid: UUID


@dataclass
class GetUserByUUIDUseCase(UseCase[GetUserByUUIDRequest, UserDTO]):
    user_repository: BaseUserRepository

    async def __call__(self, request: GetUserByUUIDRequest) -> UserDTO:
        logger.info(
            "Запрос на получение пользователя по UUID",
            extra={"user_uuid": str(request.user_uuid)}
        )

        user = await self.user_repository.get_by_uuid(request.user_uuid)

        if user is None:
            logger.warning(
                "Пользователь с указанным UUID не найден",
                extra={"user_uuid": str(request.user_uuid)}
            )
            raise UserNotFound()

        logger.info(
            "Пользователь найден",
            extra={
                "user_uuid": str(user.uuid),
                "tg_id": user.tg_id,
            }
        )

        return UserDTO.from_entity(user)
