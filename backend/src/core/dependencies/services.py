from dishka import Provider, provide, Scope

from src.core.config import AppSettings
from src.core.config import settings    
from src.application.services.game_logic import GameLogicService
from src.application.services.stars_payment.base import StarsPaymentServiceBase
from src.application.services.stars_payment.fake import FakeStarsPaymentService
from src.application.services.stars_payment.impl import ImplStarsPaymentService
from src.infrastructure.security.jwt import JWTService



class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def jwt_service(self) -> JWTService:
        return JWTService(
            secret=settings.app.secret_key,
            algorithm=settings.app.algorithm,
            ttl_minutes=settings.app.expare_minutes,
        )

    @provide
    def game_logic_service(self) -> GameLogicService:
        return GameLogicService()

    @provide
    def stars_payment_service(
        self,
        settings: AppSettings,
    ) -> StarsPaymentServiceBase:

        if settings.app.use_fake_stars:
            return FakeStarsPaymentService()

        return ImplStarsPaymentService(settings.bot.token)
    
