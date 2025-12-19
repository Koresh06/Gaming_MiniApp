from dishka import provide, Provider, Scope

from src.core.mediator.mediator import Mediator

from src.application.use_cases.auth.auth import TelegramAuthRequest, TelegramAuthUseCase

from src.application.use_cases.user.create import CreateUserRequest, CreateUserUseCase
from src.application.use_cases.user.get_by_uuid import GetUserByUUIDRequest, GetUserByUUIDUseCase
from src.application.use_cases.user.get_by_tg_id import GetUserByTgIdRequest, GetUserByTgIdUseCase

from src.application.use_cases.bet.create import CreateBetRequest, CreateBetUseCase
from src.application.use_cases.payment.init import InitPaymentRequest, InitPaymentUseCase
from src.application.use_cases.bet.get_by_uuid import GetBetByUUIDRequest, GetBetByUUIDUseCase
from src.application.use_cases.bet.update import UpdateBetStatusRequest, UpdateBetStatusUseCase

from src.application.use_cases.game_round.get_round import GetGameRoundRequest, GetGameRoundUseCase
from src.application.use_cases.game_round.play_game import PlayGameRequest, PlayGameUseCase

from src.application.use_cases.game.get_outcome_settings import GetOutcomeSettingsRequest, GetOutcomeSettingsUseCase
from src.application.use_cases.game.update_outcome_settings import UpdateGameOutcomeSettingsRequest, UpdateGameOutcomeSettingsUseCase

from src.application.use_cases.payout.process import ProcessPayoutRequest, ProcessPayoutUseCase
from src.application.use_cases.payout.update import UpdatePayoutStatusRequest, UpdatePayoutStatusUseCase

from src.application.use_cases.game.get_all import GetGamesRequest, GetGamesUseCase


class MediatorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def mediator(
        self,
        # auth
        telegram_auth_uc: TelegramAuthUseCase,

        # users
        create_user_uc: CreateUserUseCase,
        get_user_by_uuid_uc: GetUserByUUIDUseCase,
        get_user_by_tg_id_uc: GetUserByTgIdUseCase,

        # bets
        create_bet_uc: CreateBetUseCase,
        init_payment_uc: InitPaymentUseCase,
        get_bet_by_uuid_uc: GetBetByUUIDUseCase,
        update_bet_status_uc: UpdateBetStatusUseCase,

        # games
        get_game_round_uc: GetGameRoundUseCase,
        play_game_uc: PlayGameUseCase,
        get_games_uc: GetGamesUseCase,

        # outcomes
        get_outcome_settings_uc: GetOutcomeSettingsUseCase,
        update_game_outcome_settings_uc: UpdateGameOutcomeSettingsUseCase,

        # payouts
        process_payout_uc: ProcessPayoutUseCase,
        update_payout_status_uc: UpdatePayoutStatusUseCase,
    ) -> Mediator:

        mediator = Mediator()

        # auth
        mediator.register(TelegramAuthRequest, telegram_auth_uc)

        # users
        mediator.register(CreateUserRequest, create_user_uc)
        mediator.register(GetUserByUUIDRequest, get_user_by_uuid_uc)
        mediator.register(GetUserByTgIdRequest, get_user_by_tg_id_uc)

        # bets
        mediator.register(CreateBetRequest, create_bet_uc)
        mediator.register(InitPaymentRequest, init_payment_uc)
        mediator.register(GetBetByUUIDRequest, get_bet_by_uuid_uc)
        mediator.register(UpdateBetStatusRequest, update_bet_status_uc)

        # games
        mediator.register(GetGameRoundRequest, get_game_round_uc)
        mediator.register(PlayGameRequest, play_game_uc)
        mediator.register(GetGamesRequest, get_games_uc)

        # outcomes
        mediator.register(GetOutcomeSettingsRequest, get_outcome_settings_uc)
        mediator.register(
            UpdateGameOutcomeSettingsRequest,
            update_game_outcome_settings_uc,
        )

        # payouts
        mediator.register(ProcessPayoutRequest, process_payout_uc)
        mediator.register(UpdatePayoutStatusRequest, update_payout_status_uc)

        return mediator