import logging
from uuid import UUID
from dataclasses import dataclass

from src.application.dtos.bet import BetDTO
from src.application.exceptions.bet import BetNotFound
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.infrastructure.repositories.bet.base import BaseBetRepository


logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=False)
class GetBetByUUIDRequest(UseCaseRequest):
    bet_uuid: UUID


@dataclass
class GetBetByUUIDUseCase(UseCase[GetBetByUUIDRequest, BetDTO]):
    bet_repository: BaseBetRepository

    async def __call__(self, request: GetBetByUUIDRequest) -> BetDTO:
        logger.info(
            "Получен запрос на получение ставки по UUID",
            extra={
                "bet_uuid": str(request.bet_uuid),
            }
        )

        try:
            bet = await self.bet_repository.get_by_uuid(request.bet_uuid)
        except Exception as e:
            logger.error(
                "Ошибка при запросе ставки из базы данных",
                extra={
                    "bet_uuid": str(request.bet_uuid),
                    "exception": str(e),
                }
            )
            raise

        if bet is None:
            logger.warning(
                "Ставка не найдена",
                extra={
                    "bet_uuid": str(request.bet_uuid),
                }
            )
            raise BetNotFound()

        logger.info(
            "Ставка успешно найдена",
            extra={
                "bet_uuid": str(bet.uuid),
                "user_uuid": str(bet.user_uuid),
                "game_code": bet.game_code.value,
                "amount": bet.amount,
                "status": bet.status.value,
            }
        )

        dto = BetDTO.from_entity(bet)

        logger.info(
            "Данные ставки успешно возвращены",
            extra={
                "bet_uuid": str(dto.uuid),
                "status": dto.status.value,
            }
        )

        return dto
