from core.quiz_cards import QuizCardFactory


def test_create_cards():
    definitions = [
        ("A", "a", "q1"),
        ("B", "b", "q2"),
        ("C", "c", "q3"),
        ("D", "d", "q4"),
    ]

    cards = QuizCardFactory.create(definitions)

    assert len(cards) == 4


def test_not_enough_definitions():
    definitions = [
        ("A", "a", "q1"),
        ("B", "b", "q2"),
    ]

    cards = QuizCardFactory.create(definitions)

    assert cards == []


def test_card_has_four_options():
    definitions = [
        ("A", "a", "q1"),
        ("B", "b", "q2"),
        ("C", "c", "q3"),
        ("D", "d", "q4"),
    ]

    cards = QuizCardFactory.create(definitions)

    assert len(cards[0].options) == 4