from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import AppSettings
from src.presentation.api.v1.middlewares.rate_limit import RateLimitingMiddleware
from src.presentation.api.v1.middlewares.telegram_signature import TelegramSignatureMiddleware


def setup_middlewares(
    app: FastAPI,
    settings: AppSettings
):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RateLimitingMiddleware)
    app.add_middleware(
        TelegramSignatureMiddleware,
        secret_token=settings.bot.secret_token,
    )