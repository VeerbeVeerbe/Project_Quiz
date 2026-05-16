"""
Профилирование проекта Quiz2notes.
"""

import statistics
import time
from timeit import repeat

from core.definitions import DefinitionExtractor
from core.local_ai_definitions import LocalAIDefinitionExtractor
from core.quiz_cards import QuizCardFactory
from storage.storage import (
    add_correct_answer,
    add_wrong_answer,
    get_user_stats,
)


TEST_TEXT = """
Стек — это структура данных.
Очередь — это структура данных.
Граф — это множество вершин и ребер.
Дерево — это иерархическая структура данных.
Бинарное дерево — это дерево,
в котором у вершины не более двух потомков.
Хеш-таблица — это структура данных
для хранения пар ключ-значение.
""" * 50


def benchmark(name: str, func, iterations: int = 100) -> None:
    """
    Benchmark функции.
    """
    times = repeat(func, repeat=5, number=iterations)

    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\n{name}")
    print("-" * 50)
    print(f"Iterations: {iterations}")
    print(f"Average: {avg_time:.6f} sec")
    print(f"Min: {min_time:.6f} sec")
    print(f"Max: {max_time:.6f} sec")
    print(f"Per call: {avg_time / iterations:.8f} sec")


def benchmark_regex_extraction() -> None:
    """
    Benchmark regex extraction.
    """
    DefinitionExtractor.extract(TEST_TEXT)


def benchmark_ai_extraction() -> None:
    """
    Benchmark AI extraction.
    """
    extractor = LocalAIDefinitionExtractor()

    extractor.split_text(TEST_TEXT)


def benchmark_quiz_generation() -> None:
    """
    Benchmark quiz generation.
    """
    definitions = DefinitionExtractor.extract(TEST_TEXT)

    QuizCardFactory.create(definitions)


def benchmark_storage() -> None:
    """
    Benchmark TinyDB operations.
    """
    add_correct_answer(1)
    add_wrong_answer(1, "Что такое стек?")

    get_user_stats(1)


def benchmark_full_pipeline() -> None:
    """
    Benchmark полного pipeline.
    """
    definitions = DefinitionExtractor.extract(TEST_TEXT)

    cards = QuizCardFactory.create(definitions)

    for _ in cards:
        add_correct_answer(1)


if __name__ == "__main__":
    total_start = time.perf_counter()

    benchmark(
        "Regex Extraction",
        benchmark_regex_extraction,
    )

    benchmark(
        "AI Extraction",
        benchmark_ai_extraction,
    )

    benchmark(
        "Quiz Generation",
        benchmark_quiz_generation,
    )

    benchmark(
        "Storage Operations",
        benchmark_storage,
    )

    benchmark(
        "Full Pipeline",
        benchmark_full_pipeline,
    )

    total_end = time.perf_counter()

    print("\n" + "=" * 50)

    print(
        f"Total profiling time: "
        f"{total_end - total_start:.4f} sec"
    )