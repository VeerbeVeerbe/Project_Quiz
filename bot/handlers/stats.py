"""
Обработчик статистики пользователя.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from storage.storage import get_user_stats


router = Router()


@router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    """
    Показывает статистику пользователя.
    """
    user = message.from_user

    if user is None:
        return

    stats = get_user_stats(user.id)
    mistakes = stats["mistakes"]
    mistakes_text = "\n".join(f"- {term}" for term in mistakes)

    if not mistakes_text:
        mistakes_text = "Нет ошибок."

    await message.answer(
        "📊 Статистика\n\n"
        f"✅ Правильных ответов: {stats['correct']}\n"
        f"❌ Неправильных ответов: {stats['wrong']}\n\n"
        f"Ошибки:\n{mistakes_text}"
    )