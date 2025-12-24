"""
Лабораторная работа по статистике. Вариант 16.
Доверительные интервалы для нормального распределения.
"""

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def generate_sample(a: float, sigma: float, n: int, seed: int = 42) -> tuple:
    """
    Генерирует выборку из нормального распределения.

    Args:
        a: Математическое ожидание
        sigma: Стандартное отклонение
        n: Объем выборки
        seed: Seed для воспроизводимости

    Returns:
        Кортеж (выборка, выборочное среднее, выборочная дисперсия, выборочное СКО)
    """
    np.random.seed(seed)
    sample = np.random.normal(loc=a, scale=sigma, size=n)
    x_bar = np.mean(sample)
    s2 = np.var(sample, ddof=1)
    s = np.sqrt(s2)
    return sample, x_bar, s2, s


def mean_ci_known_variance(x_bar: float, sigma: float,
                           n: int, gamma: float) -> tuple:
    """
    Доверительный интервал для матожидания при известной дисперсии.

    Args:
        x_bar: Выборочное среднее
        sigma: Известное стандартное отклонение
        n: Объем выборки
        gamma: Уровень доверия

    Returns:
        Кортеж (нижняя граница, верхняя граница, длина интервала)
    """
    z = stats.norm.ppf((1 + gamma) / 2)
    delta = z * sigma / np.sqrt(n)
    lower = x_bar - delta
    upper = x_bar + delta
    width = upper - lower
    return lower, upper, width


def mean_ci_unknown_variance(x_bar: float, s: float,
                             n: int, gamma: float) -> tuple:
    """
    Доверительный интервал для матожидания при неизвестной дисперсии.

    Args:
        x_bar: Выборочное среднее
        s: Выборочное стандартное отклонение
        n: Объем выборки
        gamma: Уровень доверия

    Returns:
        Кортеж (нижняя граница, верхняя граница, длина интервала)
    """
    t_crit = stats.t.ppf((1 + gamma) / 2, df=n - 1)
    delta = t_crit * s / np.sqrt(n)
    lower = x_bar - delta
    upper = x_bar + delta
    width = upper - lower
    return lower, upper, width


def variance_ci(s2: float, n: int, gamma: float) -> tuple:
    """
    Доверительный интервал для дисперсии.

    Args:
        s2: Выборочная дисперсия
        n: Объем выборки
        gamma: Уровень доверия

    Returns:
        Кортеж (нижняя граница, верхняя граница, длина интервала)
    """
    chi2_lower = stats.chi2.ppf((1 - gamma) / 2, df=n - 1)
    chi2_upper = stats.chi2.ppf((1 + gamma) / 2, df=n - 1)
    lower = (n - 1) * s2 / chi2_upper
    upper = (n - 1) * s2 / chi2_lower
    width = upper - lower
    return lower, upper, width


def estimate_gamma_star(a: float, sigma: float,
                        n: int, gamma: float, m: int) -> float:
    """
    Оценка фактической надежности gamma* через Monte-Carlo симуляцию.

    Args:
        a: Истинное математическое ожидание
        sigma: Истинное стандартное отклонение
        n: Объем выборки
        gamma: Теоретический уровень доверия
        m: Количество симуляций

    Returns:
        Оценка gamma*
    """
    cover_count = 0

    for _ in range(m):
        sample = np.random.normal(loc=a, scale=sigma, size=n)
        x_bar = np.mean(sample)
        s2 = np.var(sample, ddof=1)
        s = np.sqrt(s2)

        t_crit = stats.t.ppf((1 + gamma) / 2, df=n - 1)
        margin = t_crit * s / np.sqrt(n)

        lower = x_bar - margin
        upper = x_bar + margin

        if lower <= a <= upper:
            cover_count += 1

    return cover_count / m


def find_gamma_for_deviation(n: int, delta_ratio: float = 0.25) -> float:
    """
    Находит надежность gamma, гарантирующую отклонение |x̄ - a| ≤ delta_ratio * S.

    Args:
        n: Объем выборки
        delta_ratio: Отношение отклонения к стандартному отклонению

    Returns:
        Требуемая надежность gamma
    """
    t_needed = delta_ratio * np.sqrt(n)
    gamma_needed = 2 * stats.t.cdf(t_needed, df=n - 1) - 1
    return gamma_needed


def find_n_for_deviation(gamma: float, delta_ratio: float = 0.25) -> int:
    """
    Находит объем выборки, гарантирующий отклонение |x̄ - a| ≤ delta_ratio * S.

    Args:
        gamma: Требуемый уровень доверия
        delta_ratio: Отношение отклонения к стандартному отклонению

    Returns:
        Необходимый объем выборки
    """
    best_n = 10
    best_diff = float('inf')

    for n_candidate in range(10, 200):
        df = n_candidate - 1
        t_crit = stats.t.ppf((1 + gamma) / 2, df)
        right_side = delta_ratio * np.sqrt(n_candidate)
        diff = abs(t_crit - right_side)

        if diff < best_diff:
            best_diff = diff
            best_n = n_candidate

    return best_n


def plot_ci_length_vs_gamma(a: float, sigma: float, s: float,
                            s2: float, n: int) -> None:
    """
    Строит график длины доверительного интервала от надежности gamma.

    Args:
        a: Математическое ожидание
        sigma: Стандартное отклонение
        s: Выборочное стандартное отклонение
        s2: Выборочная дисперсия
        n: Объем выборки
    """
    gammas = np.linspace(0.50, 0.999, 60)
    length_mean_known = []
    length_mean_unknown = []
    length_var = []

    for g in gammas:
        z_g = stats.norm.ppf((1 + g) / 2)
        length_mean_known.append(2 * z_g * sigma / np.sqrt(n))

        t_g = stats.t.ppf((1 + g) / 2, df=n - 1)
        length_mean_unknown.append(2 * t_g * s / np.sqrt(n))

        chi_lower = stats.chi2.ppf((1 - g) / 2, df=n - 1)
        chi_upper = stats.chi2.ppf((1 + g) / 2, df=n - 1)
        length_var.append((n - 1) * s2 * (1 / chi_lower - 1 / chi_upper))

    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    plt.plot(gammas, length_mean_known)
    plt.title('Длина ДИ (ср., σ известна)')
    plt.xlabel('gamma')
    plt.grid(alpha=0.3)

    plt.subplot(1, 3, 2)
    plt.plot(gammas, length_mean_unknown)
    plt.title('Длина ДИ (ср., σ неизвестна)')
    plt.xlabel('gamma')
    plt.grid(alpha=0.3)

    plt.subplot(1, 3, 3)
    plt.plot(gammas, length_var)
    plt.title('Длина ДИ (σ²)')
    plt.xlabel('gamma')
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_ci_length_vs_n(a: float, sigma: float, s: float,
                        s2: float, gamma: float) -> None:
    """
    Строит график длины доверительного интервала от объема выборки.

    Args:
        a: Математическое ожидание
        sigma: Стандартное отклонение
        s: Выборочное стандартное отклонение
        s2: Выборочная дисперсия
        gamma: Уровень доверия
    """
    ns = np.arange(10, 201, 5)
    len_mean_known_n = []
    len_mean_unknown_n = []
    len_var_n = []

    for n_val in ns:
        z_g = stats.norm.ppf((1 + gamma) / 2)
        len_mean_known_n.append(2 * z_g * sigma / np.sqrt(n_val))

        t_val = stats.t.ppf((1 + gamma) / 2, df=n_val - 1)
        len_mean_unknown_n.append(2 * t_val * s / np.sqrt(n_val))

        chi_lower = stats.chi2.ppf((1 - gamma) / 2, df=n_val - 1)
        chi_upper = stats.chi2.ppf((1 + gamma) / 2, df=n_val - 1)
        len_var_n.append((n_val - 1) * s2 * (1 / chi_lower - 1 / chi_upper))

    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    plt.plot(ns, len_mean_known_n)
    plt.title('Длина ДИ (ср., σ известна) vs n')
    plt.xlabel('n')
    plt.grid(alpha=0.3)

    plt.subplot(1, 3, 2)
    plt.plot(ns, len_mean_unknown_n)
    plt.title('Длина ДИ (ср., σ неизвестна) vs n')
    plt.xlabel('n')
    plt.grid(alpha=0.3)

    plt.subplot(1, 3, 3)
    plt.plot(ns, len_var_n)
    plt.title('Длина ДИ (σ²) vs n')
    plt.xlabel('n')
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


def main() -> None:
    """Основная функция для запуска анализа."""
    # Параметры вашего варианта (16)
    a = 1.0
    sigma2 = 2.0
    sigma = np.sqrt(sigma2)
    gamma = 0.925
    n = 10
    m_simulations = 1750

    print("=" * 70)
    print(f"ВАРИАНТ 16: (a={a}, σ²={sigma2}, gamma={gamma}, n={n})")
    print("=" * 70)

    # Формируем выборку
    sample, x_bar, s2, s = generate_sample(a, sigma, n, seed=42)

    print("\nЧАСТЬ I")
    print("-" * 30)
    print(f"Объем выборки n = {n}")
    print(f"Выборочное среднее x̄ = {x_bar:.6f}")
    print(f"Выборочная дисперсия s² = {s2:.6f}")
    print(f"Выборочное σ (s) = {s:.6f}")
    print(f"Истинные параметры: a = {a}, σ² = {sigma2}, σ = {sigma:.6f}")

    # 1.1 ДИ для матожидания при известной дисперсии
    print("\n1.1 ДИ для матожидания (σ известна)")
    ci_known = mean_ci_known_variance(x_bar, sigma, n, gamma)
    print(f"ДИ = [{ci_known[0]:.6f}, {ci_known[1]:.6f}], длина = {ci_known[2]:.6f}")

    # 1.2 ДИ для матожидания при неизвестной дисперсии
    print("\n1.2 ДИ для матожидания (σ неизвестна)")
    ci_unknown = mean_ci_unknown_variance(x_bar, s, n, gamma)
    print(f"ДИ = [{ci_unknown[0]:.6f}, {ci_unknown[1]:.6f}], длина = {ci_unknown[2]:.6f}")

    # 1.3 ДИ для дисперсии
    print("\n1.3 ДИ для дисперсии σ²")
    ci_var = variance_ci(s2, n, gamma)
    print(f"ДИ = [{ci_var[0]:.6f}, {ci_var[1]:.6f}], длина = {ci_var[2]:.6f}")
    print(f"Покрывает ли интервал истинное σ² = {sigma2}? -> {ci_var[0] <= sigma2 <= ci_var[1]}")

    # 4. Моделирование для оценки gamma*
    print("\n4. Моделирование M выборок для оценки gamma*")
    gamma_star = estimate_gamma_star(a, sigma, n, gamma, m_simulations)
    print(f"M = {m_simulations}, оценка gamma* = {gamma_star:.6f}")
    print(f"Истинное gamma = {gamma}, отклонение = {abs(gamma_star - gamma):.6f}")

    # Вопрос 1
    print("\n--- ВОПРОС 1 ---")
    gamma_needed = find_gamma_for_deviation(n, 0.25)
    print(f"gamma ≈ {gamma_needed:.4f} ({gamma_needed * 100:.1f}%)")

    # Вопрос 2
    print("\n--- ВОПРОС 2 ---")
    n_required = find_n_for_deviation(gamma, 0.25)
    print(f"n ≈ {n_required}")

    # Построение графиков
    plot_ci_length_vs_gamma(a, sigma, s, s2, n)
    plot_ci_length_vs_n(a, sigma, s, s2, gamma)

    print("\nКонец работы.")


if __name__ == "__main__":
    main()