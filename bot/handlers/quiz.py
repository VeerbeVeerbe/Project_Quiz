"""
Обработчики прохождения квиза.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from storage.storage import (
    add_correct_answer,
    add_wrong_answer,
    user_progress,
    user_quizzes,
)

router = Router()


@router.message(Command("quiz"))
async def start_quiz(message: Message) -> None:
    """
    Запускает квиз для пользователя.
    """
    user = message.from_user

    if user is None:
        return

    cards = user_quizzes.get(user.id)

    if not cards:
        await message.answer("Сначала загрузи конспект.")
        return

    user_progress[user.id] = 0
    card = cards[0]

    await message.answer(
        card.question,
        reply_markup=card.build_keyboard(),
    )


@router.message(Command("stop"))
async def stop_quiz(message: Message) -> None:
    """
    Досрочно завершает квиз.
    """
    user = message.from_user

    if user is None:
        return

    if user.id not in user_progress:
        await message.answer("Сейчас нет активного квиза.")
        return

    user_progress.pop(user.id, None)

    await message.answer("🛑 Квиз остановлен.")


@router.callback_query(lambda callback: callback.data.startswith("answer:"))
async def answer_handler(callback: CallbackQuery) -> None:
    """
    Обрабатывает выбранный пользователем вариант ответа.
    """
    user = callback.from_user
    cards = user_quizzes.get(user.id)

    if not cards or callback.message is None or callback.data is None:
        await callback.answer()
        return

    current_index = user_progress.get(user.id, 0)

    if current_index >= len(cards):
        await callback.answer()
        return

    card = cards[current_index]

    _, option_index_text = callback.data.split(":")
    option_index = int(option_index_text)

    if card.is_correct_option(option_index):
        add_correct_answer(user.id)
        await callback.message.answer("✅ Правильно")
    else:
        add_wrong_answer(user.id, card.question)
        await callback.message.answer("❌ Неправильно")

    next_index = current_index + 1

    if next_index >= len(cards):
        user_progress.pop(user.id, None)
        await callback.message.answer("🎉 Квиз завершен!")
        await callback.answer()
        return

    user_progress[user.id] = next_index
    next_card = cards[next_index]

    await callback.message.answer(
        next_card.question,
        reply_markup=next_card.build_keyboard(),
    )

    await callback.answer()