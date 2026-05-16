"""
Модуль генерации карточек квиза.
"""

import random

from models.quiz_card import QuizCard


class QuizCardFactory:
    """
    Создает карточки квиза.
    """

    MIN_DEFINITIONS = 4

    @classmethod
    def create(cls, definitions: list[tuple[str, str, str]]) -> list[QuizCard]:
        """
        Создает карточки по найденным определениям.
        """
        if len(definitions) < cls.MIN_DEFINITIONS:
            return []

        cards: list[QuizCard] = []

        for index, (term, definition, question) in enumerate(definitions):
            wrong_answers = [
                other_definition
                for (other_term, other_definition, other_question) in definitions
                if other_term != term
            ]

            options = [definition]
            options.extend(random.sample(wrong_answers, 3))
            random.shuffle(options)

            cards.append(
                QuizCard(
                    question=question,
                    options=options,
                    correct_answer=definition,
                    index=index,
                )
            )

        return cards