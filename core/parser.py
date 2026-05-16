from pathlib import Path

from exceptions import EmptyFileError, UnsupportedFileError

SUPPORTED_EXTENSIONS = {".txt", ".md"}


def validate_extension(filename: str) -> None:
    """
    Проверяет расширение файла.
    """
    if not any(filename.endswith(extension)
               for extension in SUPPORTED_EXTENSIONS):
        raise UnsupportedFileError("Поддерживаются только .txt и .md")


def validate_text(text: str) -> None:
    """
    Проверяет текст на пустоту.
    """
    if not text.strip():
        raise EmptyFileError("Файл пуст.")


def read_text_file(file_path: str) -> str:
    """
    Читает текстовый файл.

    Args:
        file_path: Путь к файлу.

    Returns:
        Текст из файла.

    Raises:
        EmptyFileError: Если файл пустой.
    """
    text = Path(file_path).read_text(encoding="utf-8")
    validate_text(text)

    return text