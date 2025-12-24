"""
Интеграционный тест полного workflow.
Покрывает основные сценарии использования модуля.
"""

import pytest
import numpy as np
from lab_statistics import (
    generate_sample,
    mean_ci_known_variance,
    mean_ci_unknown_variance,
    variance_ci,
    estimate_gamma_star,
    find_gamma_for_deviation,
    find_n_for_deviation,
)


class TestIntegration:
    """Интеграционные тесты полного workflow."""

    def test_complete_workflow_small_sample(self):
        """Полный workflow для маленькой выборки."""
        # Параметры
        a = 0.0
        sigma = 1.0
        n = 20
        gamma = 0.95
        m = 100

        # 1. Генерация выборки
        sample, x_bar, s2, s = generate_sample(a, sigma, n, seed=42)

        # Проверка выборки
        assert len(sample) == n
        assert np.isclose(x_bar, np.mean(sample))
        assert np.isclose(s2, np.var(sample, ddof=1))
        assert np.isclose(s, np.sqrt(s2))

        # 2. Доверительные интервалы
        ci_known = mean_ci_known_variance(x_bar, sigma, n, gamma)
        ci_unknown = mean_ci_unknown_variance(x_bar, s, n, gamma)
        ci_var = variance_ci(s2, n, gamma)

        # Проверка интервалов
        assert ci_known[0] < ci_known[1]
        assert ci_unknown[0] < ci_unknown[1]
        assert ci_var[0] < ci_var[1]

        # Выборочное среднее должно быть внутри интервалов для среднего
        assert ci_known[0] <= x_bar <= ci_known[1]
        assert ci_unknown[0] <= x_bar <= ci_unknown[1]

        # 3. Оценка gamma* (упрощенная версия для теста)
        gamma_star = estimate_gamma_star(a, sigma, n, gamma, m)
        assert 0 <= gamma_star <= 1

        # 4. Поиск gamma для отклонения
        gamma_for_dev = find_gamma_for_deviation(n, 0.25)
        assert 0 <= gamma_for_dev <= 1

        # 5. Поиск n для отклонения
        n_req = find_n_for_deviation(gamma, 0.25)
        assert 10 <= n_req <= 200

        print(f"✅ Интеграционный тест пройден: x̄={x_bar:.3f}, s²={s2:.3f}")

    def test_edge_case_zero_variance(self):
        """Тест граничного случая с очень маленькой дисперсией."""
        a = 5.0
        sigma = 0.001  # Почти нулевая дисперсия
        n = 10
        gamma = 0.95

        sample, x_bar, s2, s = generate_sample(a, sigma, n, seed=123)

        # При почти нулевой дисперсии интервалы должны быть очень узкими
        ci_known = mean_ci_known_variance(x_bar, sigma, n, gamma)
        ci_unknown = mean_ci_unknown_variance(x_bar, s, n, gamma)

        width_known = ci_known[2]
        width_unknown = ci_unknown[2]

        assert width_known < 0.01
        assert width_unknown < 0.01

    def test_large_sample_behavior(self):
        """Тест поведения при большой выборке."""
        a = 10.0
        sigma = 2.0
        n = 500  # Большая выборка
        gamma = 0.95

        sample, x_bar, s2, s = generate_sample(a, sigma, n, seed=42)

        ci_known = mean_ci_known_variance(x_bar, sigma, n, gamma)
        ci_unknown = mean_ci_unknown_variance(x_bar, s, n, gamma)

        # При большой выборке интервалы должны быть узкими
        assert ci_known[2] < 0.5
        assert ci_unknown[2] < 0.5

        # При большой выборке t-распределение близко к нормальному
        diff_width = abs(ci_known[2] - ci_unknown[2])
        assert diff_width < 0.1