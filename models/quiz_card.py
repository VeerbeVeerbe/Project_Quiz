"""
Модель карточки квиза.
"""

from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dataclass
class QuizCard:
    """
    Карточка квиза с вопросом и вариантами ответа.
    """

    question: str
    options: list[str]
    correct_answer: str
    index: int

    def build_keyboard(self) -> InlineKeyboardMarkup:
        """
        Создает inline-клавиатуру с вариантами ответа.
        """
        buttons = []

        for option_index, option in enumerate(self.options):
            buttons.append(
                [
                    InlineKeyboardButton(text=option, callback_data=f"answer:{option_index}")
                ]
            )

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    def is_correct_option(self, option_index: int) -> bool:
        """
        Проверяет, является ли выбранный вариант правильным.
        """
        return self.options[option_index] == self.correct_answer