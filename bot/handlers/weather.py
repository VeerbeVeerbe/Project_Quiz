"""
Обработчик команды /weather для вывода текущей погоды.
"""

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

CITY = "Moscow"
WEATHER_URL = f"https://wttr.in/{CITY}?format=Погода+в+%l:+%c+%t,+%C\nОщущается+как:+%f\nВетер:+%w\nВлажность:+%h"

@router.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    """
    Получает текущую погоду с wttr.in и отправляет её пользователю.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_URL, timeout=10) as response:
                if response.status == 200:
                    weather_text = await response.text()
                    await message.answer(weather_text)
                else:
                    await message.answer("❌ Не удалось получить данные о погоде. Попробуйте позже.")
    except Exception as e:

        await message.answer("⚠️ Произошла ошибка при подключении к сервису погоды.")