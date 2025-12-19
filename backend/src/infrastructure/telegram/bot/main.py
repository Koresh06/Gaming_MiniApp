import logging

from aiohttp import web
from aiohttp.web import Application
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from src.core.dependencies.providers import make_base_providers
from src.core.dependencies.use_cases import UseCasesProvider
from src.core.config import settings
from src.infrastructure.telegram.bot.shutdown import on_shutdown
from src.infrastructure.telegram.bot.startup import on_startup

from src.infrastructure.telegram.bot.handlers.router import router


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


def create_app() -> None:
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    container = make_async_container(*make_base_providers(), AiogramProvider())
    setup_dishka(container=container, router=dp, auto_inject=True)

    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.bot.secret_token,
    )
    webhook_requests_handler.register(app, path=settings.bot.webhook_route)

    setup_application(app, dp, bot=bot)

    web.run_app(
        app,
        host=settings.bot.web_server_host,
        port=settings.bot.web_server_port,
    )


if __name__ == "__main__":
    logger.info("Starting bot")
    create_app()