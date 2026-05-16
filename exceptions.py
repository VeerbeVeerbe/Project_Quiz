"""
Пользовательские исключения проекта.
"""


class UnsupportedFileError(Exception):
    """
    Ошибка неподдерживаемого формата файла.
    """


class EmptyFileError(Exception):
    """
    Ошибка пустого файла.
    """


class NoDefinitionsError(Exception):
    """
    Ошибка отсутствия определений в тексте.
    """