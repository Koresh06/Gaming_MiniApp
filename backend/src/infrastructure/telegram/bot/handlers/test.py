from aiogram import Router
from aiogram.types import Message


router = Router()

@router.message()
async def test_handler(message: Message) -> None:
    await message.answer(f"Webhook работает! Ты написал: {message.text}")