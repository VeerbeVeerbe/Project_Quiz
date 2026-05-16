"""
Обработчик команды /start.
"""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    Отправляет приветственное сообщение.
    """
    await message.answer(
        "Привет!\n\n"
        "Отправь .txt или .md конспект, "
        "а потом запусти квиз командой /quiz."
    )