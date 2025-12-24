"""
Параметризованные тесты для функций
find_gamma_for_deviation и find_n_for_deviation.
Покрывает функции: find_gamma_for_deviation, find_n_for_deviation
"""

import pytest
from lab_statistics import find_gamma_for_deviation, find_n_for_deviation


class TestParametricFunctions:
    """Параметризованные тесты для статистических функций."""

    @pytest.mark.parametrize("n,delta_ratio,expected_min_gamma", [
        (10, 0.25, 0.5),   # Маленькая выборка, среднее отклонение
        (30, 0.25, 0.7),   # Средняя выборка
        (100, 0.25, 0.9),  # Большая выборка
        (20, 0.1, 0.2),    # Малое отклонение
        (20, 0.5, 0.95),   # Большое отклонение
    ])


    def test_find_gamma_for_deviation_parameterized(
        self, n, delta_ratio, expected_min_gamma
    ):
        """
        ПАРАМЕТРИЗОВАННЫЙ ТЕСТ: Поиск gamma для заданного отклонения.
        Проверяет, что функция возвращает значения в разумных пределах.
        """
        gamma = find_gamma_for_deviation(n, delta_ratio)

        # Проверка диапазона
        assert 0 <= gamma <= 1

        # Проверка, что gamma не слишком мала для данных параметров
        assert gamma >= expected_min_gamma - 0.3  # С допуском

        # Для больших n и/или больших delta_ratio gamma должна быть выше
        if n == 100 and delta_ratio == 0.25:
            assert gamma > 0.8

    @pytest.mark.parametrize("gamma,delta_ratio,expected_min_n", [
        (0.90, 0.25, 10),  # Средняя надежность
        (0.95, 0.25, 15),  # Высокая надежность
        (0.99, 0.25, 30),  # Очень высокая надежность
        (0.95, 0.1, 50),   # Малое отклонение
        (0.95, 0.5, 10),   # Большое отклонение
    ])


    def test_find_n_for_deviation_parameterized(
        self, gamma, delta_ratio, expected_min_n
    ):
        """
        ПАРАМЕТРИЗОВАННЫЙ ТЕСТ:
        Поиск объема выборки для заданных параметров.
        """
        n_required = find_n_for_deviation(gamma, delta_ratio)

        # Проверка, что n в допустимом диапазоне
        assert 10 <= n_required <= 200

        # Проверка, что n не слишком мало для данных параметров
        assert n_required >= expected_min_n

        # Для большей надежности и/или меньшего
        # отклонения требуется большая выборка
        if gamma == 0.99 and delta_ratio == 0.25:
            assert n_required > 20
        elif gamma == 0.95 and delta_ratio == 0.1:
            assert n_required > 40

    @pytest.mark.parametrize("test_case", [
        {"n": 10, "delta": 0.25},
        {"n": 25, "delta": 0.3},
        {"n": 50, "delta": 0.2},
        {"n": 100, "delta": 0.15},
    ])


    def test_consistency_between_functions(self, test_case):
        """
        ПАРАМЕТРИЗОВАННЫЙ ТЕСТ: Проверка согласованности между функциями.
        Если для заданных n и delta найдена gamma, то обратная функция
        должна давать похожее n для этой gamma и delta.
        """
        n = test_case["n"]
        delta = test_case["delta"]

        # Находим gamma для данных n и delta
        gamma = find_gamma_for_deviation(n, delta)

        # Теперь ищем n для найденной gamma и того же delta
        n_calculated = find_n_for_deviation(gamma, delta)

        # Найденное n должно быть близко к исходному
        # (допускаем погрешность из-за дискретного поиска)
        assert abs(n_calculated - n) <= 20