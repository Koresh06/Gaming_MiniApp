from aiogram import Bot
from aiohttp.web import Application

from src.core.config import settings


async def on_startup(app: Application, bot: Bot):
    await bot.set_webhook(
        url=settings.bot.webhook_url,
        secret_token=settings.bot.secret_token,
    )
