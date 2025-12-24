"""
Тест доверительных интервалов для среднего при неизвестной дисперсии.
Покрывает функции: mean_ci_unknown_variance
"""

import pytest
from lab_statistics import mean_ci_unknown_variance


class TestMeanCIUnknownVariance:
    """Тестирование ДИ для среднего с неизвестной дисперсией."""

    def test_basic_unknown_variance_ci(self):
        """Базовый тест расчета ДИ с неизвестной дисперсией."""
        x_bar = 15.0
        s = 3.0
        n = 30
        gamma = 0.95

        lower, upper, width = mean_ci_unknown_variance(x_bar, s, n, gamma)

        # Проверка структуры
        assert isinstance(lower, float)
        assert isinstance(upper, float)
        assert isinstance(width, float)

        # Базовые проверки
        assert lower < upper
        assert width > 0
        assert lower <= x_bar <= upper

    def test_compare_known_vs_unknown(self):
        """
        Сравнение интервалов для известной и неизвестной дисперсии.
        При больших n интервалы должны быть похожи.
        """
        x_bar = 10.0
        sigma = 2.0
        s = 2.0  # предположим, что выборочное СКО равно истинному
        n_large = 100
        gamma = 0.95

        from lab_statistics import mean_ci_known_variance
        ci_known = mean_ci_known_variance(x_bar, sigma, n_large, gamma)
        ci_unknown = mean_ci_unknown_variance(x_bar, s, n_large, gamma)

        # При больших n разница должна быть небольшой
        diff_width = abs(ci_known[2] - ci_unknown[2])
        assert diff_width < 0.1  # Эмпирический порог