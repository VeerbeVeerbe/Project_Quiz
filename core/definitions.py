import re

from exceptions import NoDefinitionsError


class DefinitionExtractor:
    """
    Извлекает определения из текста по шаблонам.
    """

    PATTERNS = [
        (
            r"(.+?)\s+—\s+это\s+(.+)",
            "Что такое {term}?",
        ),
        (
            r"(.+?)\s+—\s+(.+)",
            "Что такое {term}?",
        ),
        (
            r"(.+?)\s+называется\s+(.+)",
            "Что называется {term}?",
        ),
        (
            r"(.+?)\s+называют\s+(.+)",
            "Что называют {term}?",
        ),
        (
            r"Под\s+(.+?)\s+понимают\s+(.+)",
            "Что понимают под {term}?",
        ),
        (
            r"Под\s+(.+?)\s+будем понимать\s+(.+)",
            "Что понимают под {term}?",
        ),
        (
            r"(.+?)\s+представляет собой\s+(.+)",
            "Что представляет собой {term}?",
        ),
    ]

    @classmethod
    def extract(cls, text: str) -> list[tuple[str, str]]:
        """
        Извлекает пары термин-определение.

        Args:
            text: Исходный текст.

        Returns:
            Список пар термин-определение.

        Raises:
            NoDefinitionsError: Если определения не найдены.
        """
        definitions: list[tuple[str, str]] = []
        seen_terms: set[str] = set()

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            for pattern, question_template in cls.PATTERNS:
                match = re.search(pattern, line, re.IGNORECASE)

                if not match:
                    continue

                term = match.group(1).strip(" .:-")
                definition = match.group(2).strip(" .:-")

                if len(term.split()) > 8:
                    continue
                if len(definition.split()) < 3:
                    continue

                question = question_template.format(term=term)
                key = term.lower()

                if key not in seen_terms:
                    seen_terms.add(key)
                    definitions.append((term,definition,question))

                break

        if not definitions:
            raise NoDefinitionsError("Определения не найдены.")

        return definitions

    @staticmethod
    def remove_duplicates(
        definitions: list[tuple[str, str, str]],
    ) -> list[tuple[str, str, str]]:
        """
        Удаляет дубликаты терминов.
        """
        unique_definitions = []
        seen_terms = set()

        for term, definition, question in definitions:
            key = term.lower()

            if key in seen_terms:
                continue

            seen_terms.add(key)
            unique_definitions.append((term, definition, question))

        return unique_definitions