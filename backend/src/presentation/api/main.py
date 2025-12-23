from fastapi import FastAPI

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka, FastapiProvider

from src.utils.logging import setup_logging
from src.core.config import settings
from src.core.dependencies.providers import make_base_providers

from src.presentation.api.lifespan import lifespan
from src.presentation.api.v1.entrypoints import include_router
from src.presentation.api.v1.middlewares.setup import setup_middlewares
from src.presentation.api.exception_handler import register_exception_handlers



def create_app() -> FastAPI:
    app = FastAPI(
        title="Game API",
        description="API for game",
        version="1.0.0",
        lifespan=lifespan,
    )
    setup_logging()

    container = make_async_container(*make_base_providers(), FastapiProvider())
    setup_dishka(container=container, app=app)
    
    register_exception_handlers(app)

    setup_middlewares(app, settings)

    include_router(app)

    return app
