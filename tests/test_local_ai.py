from core.local_ai_definitions import LocalAIDefinitionExtractor


def test_split_text():
    text = "a" * 2000
    chunks = LocalAIDefinitionExtractor.split_text(text)

    assert len(chunks) > 1