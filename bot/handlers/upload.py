"""
Обработчик загрузки файлов.
"""

from pathlib import Path

from aiogram import Router
from aiogram.types import Message

from core.definitions import DefinitionExtractor
from core.parser import read_text_file
from core.quiz_cards import QuizCardFactory
from exceptions import EmptyFileError, NoDefinitionsError, UnsupportedFileError
from storage.storage import user_quizzes
from core.local_ai_definitions import LocalAIDefinitionExtractor
from storage.storage import user_definitions

router = Router()

ALLOWED_EXTENSIONS = {".txt", ".md"}
UPLOAD_DIR = Path("uploads")


def validate_file_name(file_name: str | None) -> str:
    """
    Проверяет имя и расширение файла.

    Args:
        file_name: Имя загруженного файла.

    Returns:
        Имя файла.

    Raises:
        UnsupportedFileError: Если формат файла не поддерживается.
    """
    if file_name is None:
        raise UnsupportedFileError("У файла нет имени.")

    suffix = Path(file_name).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise UnsupportedFileError("Поддерживаются только .txt и .md файлы.")

    return file_name


@router.message(lambda message: message.document)
async def upload_handler(message: Message) -> None:
    """
    Обрабатывает загруженный пользователем конспект.
    """
    try:
        document = message.document

        if document is None:
            return

        file_name = validate_file_name(document.file_name)

        UPLOAD_DIR.mkdir(exist_ok=True)

        file_info = await message.bot.get_file(document.file_id)
        file_path = UPLOAD_DIR / file_name

        await message.bot.download_file(
            file_info.file_path,
            destination=file_path,
        )

        text = read_text_file(str(file_path))
        definitions = DefinitionExtractor.extract(text)
        ai_definitions = LocalAIDefinitionExtractor.extract(text)
        definitions.extend(ai_definitions)
        definitions = DefinitionExtractor.remove_duplicates(definitions)
        cards = QuizCardFactory.create(definitions)

        if not cards:
            await message.answer(
                "Найдено меньше 4 определений. "
                "Для квиза нужно минимум 4 определения."
            )
            return

        user = message.from_user

        if user is not None:
            user_quizzes[user.id] = cards
            user_definitions[user.id] = definitions

        await message.answer(
            f"Создано карточек: {len(cards)}\n"
            "Запусти квиз командой /quiz."
        )

    except (
        UnsupportedFileError,
        EmptyFileError,
        NoDefinitionsError,
    ) as error:
        await message.answer(str(error))