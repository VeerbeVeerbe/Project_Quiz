"""
AI-извлечение определений через локальную LLM.
"""

import json
import re

import requests


class LocalAIDefinitionExtractor:
    """
    Извлекает определения с помощью локальной LLM.
    """

    URL = "http://localhost:11434/api/generate"

    MODEL = "phi3"

    CHUNK_SIZE = 800

    REQUEST_TIMEOUT = 20

    PROMPT_TEMPLATE = """
Найди определения и термины в тексте.

Обращай внимание на конструкции:

- это
- называется
- называют
- представляет собой
- понимают
- определяется как
- является

Верни только JSON.

Формат:

[
  {{
    "term": "...",
    "definition": "..."
  }}
]

Только JSON без пояснений.

Текст:

{text}
"""

    @classmethod
    def extract(cls, text: str) -> list[tuple[str, str]]:
        """
        Извлекает определения через локальную LLM.
        """
        definitions: list[tuple[str, str]] = []
        chunks = cls.split_text(text)

        for chunk in chunks:
            parsed = cls.process_chunk(chunk)

            for item in parsed:
                term = item.get("term", "").strip()
                definition = item.get("definition", "").strip()

                if not term or not definition:
                    continue

                definitions.append((term, definition))

        return cls.remove_duplicates(definitions)

    @classmethod
    def split_text(cls, text: str) -> list[str]:
        """
        Делит текст на части.
        """
        return [
            text[index:index + cls.CHUNK_SIZE]
            for index in range(0, len(text), cls.CHUNK_SIZE)
        ]

    @classmethod
    def process_chunk(cls, chunk: str) -> list[dict]:
        """
        Обрабатывает часть текста через LLM.
        """
        prompt = cls.PROMPT_TEMPLATE.format(text=chunk)
        try:
            response = requests.post(cls.URL, json={
                    "model": cls.MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0, "num_predict": 300},
                },
                timeout=cls.REQUEST_TIMEOUT,
            )

        except requests.RequestException:
            return []

        try:
            data = response.json()

        except ValueError:
            return []

        raw = data.get("response", "")
        raw = re.sub(r"```json|```", "", raw).strip()

        try:
            parsed = json.loads(raw)

        except json.JSONDecodeError:
            return []

        if not isinstance(parsed, list):
            return []

        return parsed

    @staticmethod
    def remove_duplicates(
        definitions: list[tuple[str, str]],
    ) -> list[tuple[str, str]]:
        """
        Удаляет дубликаты терминов.
        """
        unique_definitions = []
        seen_terms = set()

        for term, definition in definitions:
            key = term.lower()

            if key in seen_terms:
                continue

            seen_terms.add(key)
            unique_definitions.append((term, definition))

        return unique_definitions