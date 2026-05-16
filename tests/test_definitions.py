import pytest

from exceptions import NoDefinitionsError
from core.definitions import DefinitionExtractor


def test_extract_dash_definition():
    text = "Стек — это структура данных."

    definitions = DefinitionExtractor.extract(text)

    assert len(definitions) == 1


def test_extract_understand_pattern():
    text = (
        "Под графом понимают "
        "множество связанных вершин."
    )

    definitions = DefinitionExtractor.extract(text)

    assert len(definitions) == 1


def test_remove_duplicates():
    definitions = [
        (
            "Стек",
            "Структура данных",
            "Что такое Стек?",
        ),
        (
            "стек",
            "Другое",
            "Что такое стек?",
        ),
    ]

    unique = DefinitionExtractor.remove_duplicates(definitions)

    assert len(unique) == 1


def test_invalid_term_filtered():
    text = "Больше — это значение."

    with pytest.raises(NoDefinitionsError):
        DefinitionExtractor.extract(text)