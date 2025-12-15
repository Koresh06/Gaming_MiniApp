from fastapi import FastAPI

from src.utils.logging import setup_logging
from src.core.config import settings

from src.presentation.api.exception_handler import register_exception_handlers
from src.presentation.api.v1.middlewares.telegram_signature import TelegramSignatureMiddleware
from src.presentation.api.v1.middlewares.rate_limit import RateLimitingMiddleware
from src.presentation.api.v1.entrypoints.user import router as user_router
from src.presentation.api.v1.entrypoints.game import router as game_router
from src.presentation.api.v1.entrypoints.bet import router as bet_router
from src.presentation.api.v1.entrypoints.payout import router as payout_router
from src.presentation.api.v1.entrypoints.round import router as round_router
from src.presentation.api.v1.entrypoints.stars import router as stars_router


def include_router(app: FastAPI) -> None:
    # app.include_router(authentication_router, prefix="/auth", tags=["Аутентификация"])
    app.include_router(user_router)
    app.include_router(game_router)
    app.include_router(bet_router)
    app.include_router(payout_router)
    app.include_router(round_router)
    app.include_router(stars_router)



def create_app() -> FastAPI:
    app = FastAPI(
        title="Game API",
        description="API for game",
        version="1.0.0",
    )

    register_exception_handlers(app)
    app.add_middleware(RateLimitingMiddleware)
    app.add_middleware(
        TelegramSignatureMiddleware,
        secret_token=settings.bot.secret_token,
    )

    include_router(app)

    setup_logging()

    return app
