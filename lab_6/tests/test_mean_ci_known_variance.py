"""
Тест доверительных интервалов для среднего при известной дисперсии.
Покрывает функции: mean_ci_known_variance
"""

import pytest
import numpy as np
from lab_statistics import mean_ci_known_variance


class TestMeanCIKnownVariance:
    """Тестирование ДИ для среднего с известной дисперсией."""


    def test_basic_ci_calculation(self):
        """Базовый тест расчета доверительного интервала."""
        x_bar = 10.0
        sigma = 2.0
        n = 100
        gamma = 0.95

        lower, upper, width = mean_ci_known_variance(
            x_bar, sigma, n, gamma
        )

        # Проверка структуры
        assert isinstance(lower, float)
        assert isinstance(upper, float)
        assert isinstance(width, float)

        # Проверка логики
        assert lower < upper
        assert width > 0
        assert width == pytest.approx(upper - lower)

        # Выборочное среднее должно быть в центре интервала
        center = (lower + upper) / 2
        assert center == pytest.approx(x_bar, rel=1e-10)


    def test_ci_width_increases_with_gamma(self):
        """
        Тест: ширина интервала увеличивается с ростом gamma.
        Более высокая надежность требует более широкого интервала.
        """
        x_bar = 5.0
        sigma = 1.0
        n = 50

        # Интервалы для разных gamma
        ci_low = mean_ci_known_variance(x_bar, sigma, n, 0.90)
        ci_medium = mean_ci_known_variance(x_bar, sigma, n, 0.95)
        ci_high = mean_ci_known_variance(x_bar, sigma, n, 0.99)

        # Проверка, что ширина увеличивается с gamma
        assert ci_low[2] < ci_medium[2] < ci_high[2]

        # Центры должны быть одинаковыми
        center_low = (ci_low[0] + ci_low[1]) / 2
        center_medium = (ci_medium[0] + ci_medium[1]) / 2
        center_high = (ci_high[0] + ci_high[1]) / 2

        assert center_low == pytest.approx(center_medium)
        assert center_medium == pytest.approx(center_high)


    def test_ci_width_decreases_with_n(self):
        """
        Тест: ширина интервала уменьшается с ростом объема выборки.
        Больше данных -> более точная оценка -> уже интервал.
        """
        x_bar = 0.0
        sigma = 1.0
        gamma = 0.95

        ci_small_n = mean_ci_known_variance(
            x_bar, sigma, n=10, gamma=gamma
        )
        ci_medium_n = mean_ci_known_variance(
            x_bar, sigma, n=50, gamma=gamma
        )
        ci_large_n = mean_ci_known_variance(
            x_bar, sigma, n=200, gamma=gamma
        )

        # Проверка, что ширина уменьшается с ростом n
        assert ci_small_n[2] > ci_medium_n[2] > ci_large_n[2]