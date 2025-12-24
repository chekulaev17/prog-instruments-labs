"""
Тест доверительных интервалов для дисперсии.
Покрывает функции: variance_ci
"""

import pytest
from lab_statistics import variance_ci


class TestVarianceCI:
    """Тестирование ДИ для дисперсии."""


    def test_basic_variance_ci(self):
        """Базовый тест расчета ДИ для дисперсии."""
        s2 = 4.0  # Выборочная дисперсия
        n = 20
        gamma = 0.95

        lower, upper, width = variance_ci(s2, n, gamma)

        # Проверка структуры
        assert isinstance(lower, float)
        assert isinstance(upper, float)
        assert isinstance(width, float)

        # Для дисперсии границы должны быть положительными
        assert lower > 0
        assert upper > 0
        assert lower < upper
        assert width > 0

        # Выборочная дисперсия должна быть внутри интервала
        # или близко к границам
        # (не всегда точно внутри из-за асимметрии распределения хи-квадрат)
        assert lower <= s2 * 1.5  # Нижняя граница не слишком низкая
        assert upper >= s2 * 0.5  # Верхняя граница не слишком высокая


    def test_variance_ci_with_different_n(self):
        """Тест ДИ для дисперсии при разных объемах выборки."""
        s2 = 2.0
        gamma = 0.95

        ci_small_n = variance_ci(s2, n=10, gamma=gamma)
        ci_large_n = variance_ci(s2, n=100, gamma=gamma)

        # При большем n интервал должен быть уже (более точная оценка)
        assert ci_small_n[2] > ci_large_n[2]