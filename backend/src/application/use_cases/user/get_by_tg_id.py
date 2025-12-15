import logging
from dataclasses import dataclass

from src.application.exceptions.user import UserNotFound
from src.application.dtos.user import UserDTO
from src.application.use_cases.base import UseCaseRequest, UseCase

from src.infrastructure.repositories.user.base import BaseUserRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class GetUserByTgIdRequest(UseCaseRequest):
    tg_id: int
    # current_user_uuid: UUID 


@dataclass
class GetUserByTgIdUseCase(UseCase[GetUserByTgIdRequest, UserDTO]):
    user_repository: BaseUserRepository

    async def __call__(self, request: GetUserByTgIdRequest) -> UserDTO:
        logger.info(
            "Запрос на получение пользователя по Telegram ID",
            extra={"tg_id": request.tg_id}
        )

        user = await self.user_repository.get_by_tg_id(request.tg_id)

        if user is None:
            logger.warning(
                "Пользователь с указанным Telegram ID не найден",
                extra={"tg_id": request.tg_id}
            )
            raise UserNotFound()

        logger.info(
            "Пользователь найден",
            extra={
                "user_uuid": str(user.uuid),
                "tg_id": user.tg_id,
                "username": user.username,
            }
        )

        return UserDTO.from_entity(user)
