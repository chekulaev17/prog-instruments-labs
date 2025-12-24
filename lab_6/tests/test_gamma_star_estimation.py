"""
Продвинутый тест оценки gamma* с использованием моков.
Тестирует функцию: estimate_gamma_star
"""

import pytest
from unittest.mock import patch
import numpy as np
from lab_statistics import estimate_gamma_star


class TestGammaStarEstimation:
    """Тестирование оценки фактической надежности gamma*."""

    def test_gamma_star_range(self):
        """
        Тест, что оценка gamma* находится в допустимом диапазоне [0, 1].
        """
        a = 0.0
        sigma = 1.0
        n = 10
        gamma = 0.95
        m = 100

        gamma_star = estimate_gamma_star(a, sigma, n, gamma, m)

        assert 0 <= gamma_star <= 1

    @patch('numpy.random.normal')
    def test_gamma_star_perfect_samples(self, mock_normal):
        """
        ПРОДВИНУТЫЙ ТЕСТ: Использование моков.
        Тест с идеальными выборками (все значения равны матожиданию).
        """
        # Настраиваем мок для возврата идеальных выборок
        perfect_sample = np.array([1.0, 1.0, 1.0, 1.0, 1.0,
                                   1.0, 1.0, 1.0, 1.0, 1.0])
        mock_normal.return_value = perfect_sample

        a = 1.0
        sigma = 0.1  # Очень маленькая дисперсия
        n = 10
        gamma = 0.95
        m = 50

        gamma_star = estimate_gamma_star(a, sigma, n, gamma, m)

        # При идеальных выборках все интервалы содержат истинное значение
        # Но из-за оценки дисперсии по выборке могут быть погрешности
        # В идеале gamma_star должна быть близка к 1
        assert gamma_star >= 0.9

    @patch('numpy.random.normal')
    def test_gamma_star_extreme_samples(self, mock_normal):
        """
        ПРОДВИНУТЫЙ ТЕСТ: Использование моков.
        Тест с экстремальными выборками (сильно смещены от истинного значения).
        """
        # Выборка со средним 10 при истинном значении 1
        extreme_sample = np.array([10.0, 10.0, 10.0, 10.0, 10.0,
                                   10.0, 10.0, 10.0, 10.0, 10.0])
        mock_normal.return_value = extreme_sample

        a = 1.0  # Истинное значение
        sigma = 0.01  # Очень маленькая дисперсия для узких интервалов
        n = 10
        gamma = 0.95
        m = 30

        gamma_star = estimate_gamma_star(a, sigma, n, gamma, m)

        # При таких выборках интервалы не должны содержать истинное значение
        # Но из-за случайности может быть несколько совпадений
        assert gamma_star < 0.5  # Должно быть меньше половины