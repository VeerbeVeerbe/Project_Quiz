"""
Просмотр определений пользователя.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from storage.storage import user_definitions


router = Router()


@router.message(Command("definitions"))
async def definitions_handler(message: Message) -> None:
    """
    Показывает все определения.
    """
    user = message.from_user

    if user is None:
        return

    definitions = user_definitions.get(user.id)

    if not definitions:
        await message.answer("Сначала загрузи конспект.")
        return

    lines = ["📚 Определения\n"]

    for term, definition, question in definitions:
        lines.append(f"• {term} — {definition}")

    text = "\n".join(lines)

    if len(text) > 4000:
        text = text[:4000]

    await message.answer(text)