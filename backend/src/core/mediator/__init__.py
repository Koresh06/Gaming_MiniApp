from functools import lru_cache

from src.core.mediator.mediator import Mediator

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


@lru_cache(1)
def get_mediator() -> Mediator:
    mediator = Mediator()

    mediator.register(CreateUserRequest, CreateUserUseCase)
    mediator.register(GetUserByUUIDRequest, GetUserByUUIDUseCase)
    mediator.register(GetUserByTgIdRequest, GetUserByTgIdUseCase)

    mediator.register(CreateBetRequest, CreateBetUseCase)
    mediator.register(InitPaymentRequest, InitPaymentUseCase)
    mediator.register(GetBetByUUIDRequest, GetBetByUUIDUseCase)
    mediator.register(UpdateBetStatusRequest, UpdateBetStatusUseCase)

    mediator.register(GetGameRoundRequest, GetGameRoundUseCase)
    mediator.register(PlayGameRequest, PlayGameUseCase)

    mediator.register(GetOutcomeSettingsRequest, GetOutcomeSettingsUseCase)
    mediator.register(UpdateGameOutcomeSettingsRequest, UpdateGameOutcomeSettingsUseCase)

    mediator.register(ProcessPayoutRequest, ProcessPayoutUseCase)
    mediator.register(UpdatePayoutStatusRequest, UpdatePayoutStatusUseCase)

    mediator.register(GetGamesRequest, GetGamesUseCase)


    return mediator