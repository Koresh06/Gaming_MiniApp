from fastapi import FastAPI

from src.presentation.api.v1.entrypoints.user import router as user_router
from src.presentation.api.v1.entrypoints.game import router as game_router
from src.presentation.api.v1.entrypoints.bet import router as bet_router
from src.presentation.api.v1.entrypoints.payout import router as payout_router
from src.presentation.api.v1.entrypoints.round import router as round_router
from src.presentation.api.v1.entrypoints.auth import router as authentication_router
from src.presentation.api.v1.entrypoints.stars import router as stars_router


def include_router(app: FastAPI) -> None:
    app.include_router(authentication_router)
    app.include_router(user_router)
    app.include_router(game_router)
    app.include_router(bet_router)
    app.include_router(payout_router)
    app.include_router(round_router)
    app.include_router(stars_router)