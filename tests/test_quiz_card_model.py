from models.quiz_card import QuizCard


def test_correct_option():
    card = QuizCard(
        question="Q",
        options=["a", "b"],
        correct_answer="a",
        index=0,
    )

    assert card.is_correct_option(0)


def test_wrong_option():
    card = QuizCard(
        question="Q",
        options=["a", "b"],
        correct_answer="a",
        index=0,
    )

    assert not card.is_correct_option(1)