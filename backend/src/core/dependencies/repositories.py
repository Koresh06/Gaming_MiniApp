from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.repositories.user.sqlalchemy_repository import SQLAlchemyUserRepository

from src.infrastructure.repositories.bet.base import BaseBetRepository
from src.infrastructure.repositories.bet.sqlalchemy_repository import SQLAlchemyBetRepository

from src.infrastructure.repositories.game_round.base import BaseGameRoundRepository
from src.infrastructure.repositories.game_round.sqlalchemy_repository import SQLAlchemyGameRoundRepository

from src.infrastructure.repositories.game_outcome_settings.base import BaseGameOutcomeSettingRepository
from src.infrastructure.repositories.game_outcome_settings.sqlalchemy_repository import SQLAlchemyGameOutcomeSettingRepository

from src.infrastructure.repositories.payout.base import BasePayoutRepository
from src.infrastructure.repositories.payout.sqlalchemy_repository import SQLAlchemyPayoutRepository


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(session=session)

    @provide
    def bet_repository(self, session: AsyncSession) -> BaseBetRepository:
        return SQLAlchemyBetRepository(session=session)

    @provide
    def game_round_repository(self, session: AsyncSession) -> BaseGameRoundRepository:
        return SQLAlchemyGameRoundRepository(session=session)

    @provide
    def game_outcome_setting_repository(
        self, session: AsyncSession
    ) -> BaseGameOutcomeSettingRepository:
        return SQLAlchemyGameOutcomeSettingRepository(session=session)

    @provide
    def payout_repository(self, session: AsyncSession) -> BasePayoutRepository:
        return SQLAlchemyPayoutRepository(session=session)
