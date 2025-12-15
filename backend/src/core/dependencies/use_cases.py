from dishka import Provider, provide, Scope

# USER USE CASES
from src.application.use_cases.payment.init import InitPaymentUseCase
from src.application.use_cases.user.get_by_tg_id import GetUserByTgIdUseCase
from src.application.use_cases.user.create import CreateUserUseCase
from src.application.use_cases.user.get_by_uuid import GetUserByUUIDUseCase

# BET USE CASES
from src.application.use_cases.bet.create import CreateBetUseCase
from src.application.use_cases.bet.get_by_uuid import GetBetByUUIDUseCase
from src.application.use_cases.bet.update import UpdateBetStatusUseCase

# GAME USE CASES
from src.application.use_cases.game.get_all import GetGamesUseCase
from src.application.use_cases.game.get_outcome_settings import (
    GetOutcomeSettingsUseCase,
)
from src.application.use_cases.game.update_outcome_settings import (
    UpdateGameOutcomeSettingsUseCase,
)

# GAME ROUND USE CASES
from src.application.use_cases.game_round.play_game import PlayGameUseCase
from src.application.use_cases.game_round.get_round import GetGameRoundUseCase

# PAYOUT USE CASES
from src.application.use_cases.payout.process import ProcessPayoutUseCase
from src.application.use_cases.payout.update import UpdatePayoutStatusUseCase

from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.bet.base import BaseBetRepository
from src.infrastructure.repositories.game_outcome_settings.base import (
    BaseGameOutcomeSettingRepository,
)
from src.infrastructure.repositories.game_round.base import BaseGameRoundRepository
from src.infrastructure.repositories.payout.base import BasePayoutRepository
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.application.services.game_logic import GameLogicService
from src.application.services.stars_payment.base import StarsPaymentServiceBase


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    # ------------------
    # USER USE CASES
    # ------------------

    @provide
    def get_user_by_tg_id_use_case(
        self,
        user_repository: BaseUserRepository,
    ) -> GetUserByTgIdUseCase:
        return GetUserByTgIdUseCase(user_repository=user_repository)

    @provide
    def register_user_use_case(
        self,
        user_repository: BaseUserRepository,
        transaction_manager: TransactionManager,
    ) -> CreateUserUseCase:
        return CreateUserUseCase(
            user_repository=user_repository, transaction_manager=transaction_manager
        )

    @provide
    def get_user_by_uuid_use_case(
        self,
        user_repository: BaseUserRepository,
    ) -> GetUserByUUIDUseCase:
        return GetUserByUUIDUseCase(user_repository=user_repository)

    # ------------------
    # BET USE CASES
    # ------------------

    @provide
    def create_bet_use_case(
        self,
        bet_repository: BaseBetRepository,
        transaction_manager: TransactionManager
    ) -> CreateBetUseCase:
        return CreateBetUseCase(bet_repository=bet_repository, transaction_manager=transaction_manager)
    
    @provide
    def init_bet_payment(
        self, 
        bet_repository: BaseBetRepository,
        user_repository: BaseUserRepository,
        stars_payment_service: StarsPaymentServiceBase,
    ) -> InitPaymentUseCase:
        return InitPaymentUseCase(
            bet_repository=bet_repository,
            user_repository=user_repository,
            stars_service=stars_payment_service,
        )

    @provide
    def get_bet_by_uuid_use_case(
        self,
        bet_repository: BaseBetRepository,
    ) -> GetBetByUUIDUseCase:
        return GetBetByUUIDUseCase(bet_repository=bet_repository)

    @provide
    def update_bet_status_use_case(
        self,
        bet_repository: BaseBetRepository,
        transaction_manager: TransactionManager,
    ) -> UpdateBetStatusUseCase:
        return UpdateBetStatusUseCase(
            bet_repository=bet_repository, transaction_manager=transaction_manager
        )

    # ------------------
    # GAME USE CASES
    # ------------------

    @provide
    def get_games_use_case(self) -> GetGamesUseCase:
        return GetGamesUseCase()

    @provide
    def get_outcome_settings_use_case(
        self,
        outcome_repository: BaseGameOutcomeSettingRepository,
    ) -> GetOutcomeSettingsUseCase:
        return GetOutcomeSettingsUseCase(outcome_repository=outcome_repository)

    @provide
    def update_outcome_settings_use_case(
        self,
        outcome_repository: BaseGameOutcomeSettingRepository,
        game_logic_service: GameLogicService,
        transaction_manager: TransactionManager,
    ) -> UpdateGameOutcomeSettingsUseCase:
        return UpdateGameOutcomeSettingsUseCase(
            outcome_repository=outcome_repository,
            game_logic_service=game_logic_service,
            transaction_manager=transaction_manager,
        )

    @provide
    def play_game_use_case(
        self,
        bet_repository: BaseBetRepository,
        game_round_repository: BaseGameRoundRepository,
        game_outcome_setting_repository: BaseGameOutcomeSettingRepository,
        payout_repository: BasePayoutRepository,
        game_logic_service: GameLogicService,
        transaction_manager: TransactionManager,
    ) -> PlayGameUseCase:
        return PlayGameUseCase(
            bet_repository=bet_repository,
            round_repository=game_round_repository,         
            outcome_repository=game_outcome_setting_repository,
            payout_repository=payout_repository,
            game_logic_service=game_logic_service,
            transaction_manager=transaction_manager,
        )

    @provide
    def get_game_round_use_case(
        self,
        round_repository: BaseGameRoundRepository,
    ) -> GetGameRoundUseCase:
        return GetGameRoundUseCase(round_repository=round_repository)

    # ------------------
    # PAYOUT USE CASES
    # ------------------

    @provide
    def process_payout_use_case(
        self,
        payout_repository: BasePayoutRepository,
        round_repository: BaseGameRoundRepository,
        user_repository: BaseUserRepository,
        stars_payment_service: StarsPaymentServiceBase,
    ) -> ProcessPayoutUseCase:
        return ProcessPayoutUseCase(
            payout_repository=payout_repository,
            round_repository=round_repository,
            user_repository=user_repository,
            stars_service=stars_payment_service,
        )

    @provide
    def update_payout_status_use_case(
        self,
        payout_repository: BasePayoutRepository,
        transaction_manager: TransactionManager
    ) -> UpdatePayoutStatusUseCase:
        return UpdatePayoutStatusUseCase(payout_repository=payout_repository, transaction_manager=transaction_manager)
