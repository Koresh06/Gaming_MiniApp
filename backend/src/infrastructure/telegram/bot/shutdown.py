from aiohttp.web import Application
from aiogram import Bot


async def on_shutdown(app: Application, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()