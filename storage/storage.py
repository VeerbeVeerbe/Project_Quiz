"""
Хранилище данных пользователей.
"""

from tinydb import Query, TinyDB

from models.quiz_card import QuizCard


db = TinyDB("database.json")
stats_table = db.table("statistics")
User = Query()

user_quizzes: dict[int, list[QuizCard]] = {}
user_progress: dict[int, int] = {}
user_definitions: dict[int, list[tuple]] = {}


def get_user_stats(user_id: int) -> dict:
    """
    Возвращает статистику пользователя.
    """
    stats = stats_table.get(User.user_id == user_id)

    if stats is None:
        stats = {
            "user_id": user_id,
            "correct": 0,
            "wrong": 0,
            "mistakes": [],
        }

        stats_table.insert(stats)

    return stats


def add_correct_answer(user_id: int) -> None:
    """
    Добавляет правильный ответ.
    """
    stats = get_user_stats(user_id)
    stats["correct"] += 1
    stats_table.update(stats, User.user_id == user_id)


def add_wrong_answer(user_id: int, term: str) -> None:
    """
    Добавляет ошибку пользователя.
    """
    stats = get_user_stats(user_id)
    stats["wrong"] += 1

    if term not in stats["mistakes"]:
        stats["mistakes"].append(term)

    stats_table.update(stats, User.user_id == user_id)