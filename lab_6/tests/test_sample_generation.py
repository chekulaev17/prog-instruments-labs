"""
Тест генерации выборки и базовых статистик.
Покрывает функции: generate_sample
"""

import pytest
import numpy as np
from lab_statistics import generate_sample


class TestSampleGeneration:
    """Тестирование генерации выборок."""

    def test_sample_generation_basic(self):
        """Тест базовой генерации выборки."""
        a = 1.0
        sigma = 1.41421356  # sqrt(2)
        n = 10
        seed = 42

        sample, x_bar, s2, s = generate_sample(a, sigma, n, seed)

        # Проверка типов
        assert isinstance(sample, np.ndarray)
        assert isinstance(x_bar, float)
        assert isinstance(s2, float)
        assert isinstance(s, float)

        # Проверка размеров
        assert len(sample) == n
        assert np.mean(sample) == pytest.approx(x_bar)
        assert np.var(sample, ddof=1) == pytest.approx(s2)
        assert np.sqrt(s2) == pytest.approx(s)

        # Статистика должна быть в разумных пределах
        assert -5 < x_bar < 5
        assert s2 > 0
        assert s > 0

    def test_sample_reproducibility(self):
        """Тест воспроизводимости с одинаковым seed."""
        a = 0.0
        sigma = 1.0
        n = 5

        # Два вызова с одинаковым seed должны дать одинаковые результаты
        sample1, x_bar1, s2_1, s1 = generate_sample(a, sigma, n, seed=123)
        sample2, x_bar2, s2_2, s2 = generate_sample(a, sigma, n, seed=123)

        np.testing.assert_array_equal(sample1, sample2)
        assert x_bar1 == pytest.approx(x_bar2)
        assert s2_1 == pytest.approx(s2_2)
        assert s1 == pytest.approx(s2)

    def test_sample_different_seeds(self):
        """Тест, что разные seed дают разные выборки."""
        a = 0.0
        sigma = 1.0
        n = 10

        sample1, x_bar1, s2_1, s1 = generate_sample(a, sigma, n, seed=42)
        sample2, x_bar2, s2_2, s2 = generate_sample(a, sigma, n, seed=43)

        # Выборки должны отличаться
        with pytest.raises(AssertionError):
            np.testing.assert_array_equal(sample1, sample2)

        # Но статистики должны быть похожи (одно распределение)
        assert abs(x_bar1 - x_bar2) < 2.0
        assert abs(s2_1 - s2_2) < 2.0