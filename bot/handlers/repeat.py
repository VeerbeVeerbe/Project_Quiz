"""
Режим повторения сложных карточек.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from storage.storage import (
    get_user_stats,
    user_progress,
    user_quizzes,
)


router = Router()


@router.message(Command("repeat"))
async def repeat_handler(message: Message) -> None:
    """
    Запускает повторение карточек с ошибками.
    """
    user = message.from_user

    if user is None:
        return

    stats = get_user_stats(user.id)
    mistakes = stats["mistakes"]

    if not mistakes:
        await message.answer("У тебя пока нет карточек для повторения.")
        return

    cards = user_quizzes.get(user.id)

    if not cards:
        await message.answer("Сначала загрузи конспект.")
        return

    repeat_cards = [card for card in cards
        if any(mistake.lower() in card.question.lower() for mistake in mistakes)
    ]

    if not repeat_cards:
        await message.answer("Карточки для повторения не найдены.")
        return

    user_quizzes[user.id] = repeat_cards
    user_progress[user.id] = 0
    first_card = repeat_cards[0]

    await message.answer(
        "🔁 Режим повторения ошибок\n"
        f"Карточек: {len(repeat_cards)}"
    )

    await message.answer(
        first_card.question,
        reply_markup=first_card.build_keyboard(),
    )