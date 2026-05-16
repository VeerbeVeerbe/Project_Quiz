from storage.storage import get_user_stats


def test_create_user_stats():
    stats = get_user_stats(123)

    assert stats["correct"] == 0
    assert stats["wrong"] == 0