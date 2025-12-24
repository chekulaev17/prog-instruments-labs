import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# -----------------------
# Параметры вашего варианта (16)
# -----------------------
a = 1.0
sigma2 = 2.0
sigma = np.sqrt(sigma2)
gamma = 0.925  # надежность
n = 10
M = 1750
K = 175

np.random.seed(42)  # для воспроизводимости

print("=" * 70)
print(f"ВАРИАНТ 16: (a={a}, σ²={sigma2}, gamma={gamma}, n={n}, M={M}, K={K})")
print("=" * 70)

# -----------------------
# Формируем одну выборку (для демонстрации результатов)
# -----------------------
sample = np.random.normal(loc=a, scale=sigma, size=n)
x_bar = np.mean(sample)
s2 = np.var(sample, ddof=1)
s = np.sqrt(s2)

print("\nЧАСТЬ I")
print("-" * 30)
print(f"Объем выборки n = {n}")
print(f"Выборочное среднее x̄ = {x_bar:.6f}")
print(f"Выборочная дисперсия s² = {s2:.6f}")
print(f"Выборочное σ (s) = {s:.6f}")
print(f"Истинные параметры: a = {a}, σ² = {sigma2}, σ = {sigma:.6f}")

# -----------------------
# 1.1 Интервал для математического ожидания при известной дисперсии
# -----------------------
print("\n1.1 ДИ для матожидания (σ известна)")
z = stats.norm.ppf((1 + gamma) / 2)
delta_known = z * sigma / np.sqrt(n)
ci_known = (x_bar - delta_known, x_bar + delta_known)

# Второй способ: scipy.stats.interval
ci_known_scipy = stats.norm.interval(gamma, loc=x_bar, scale=sigma / np.sqrt(n))

print(f"Способ 1 (формула): ДИ = [{ci_known[0]:.6f}, {ci_known[1]:.6f}], длина = {ci_known[1] - ci_known[0]:.6f}")
print(
    f"Способ 2 (scipy):   ДИ = [{ci_known_scipy[0]:.6f}, {ci_known_scipy[1]:.6f}], длина = {ci_known_scipy[1] - ci_known_scipy[0]:.6f}")

# -----------------------
# 1.2 Интервальная оценка матожидания при неизвестной дисперсии
# -----------------------
print("\n1.2 ДИ для матожидания (σ неизвестна)")

# Критическое значение t
t_crit = stats.t.ppf((1 + gamma) / 2, df=n - 1)

# Способ 1: Формула
delta_unknown = t_crit * s / np.sqrt(n)
ci_unknown = (x_bar - delta_unknown, x_bar + delta_unknown)

# Способ 2: scipy.stats
ci_unknown_scipy = stats.t.interval(gamma, df=n - 1, loc=x_bar, scale=s / np.sqrt(n))

print(
    f"Способ 1 (формула): ДИ = [{ci_unknown[0]:.6f}, {ci_unknown[1]:.6f}], длина = {ci_unknown[1] - ci_unknown[0]:.6f}")
print(
    f"Способ 2 (scipy):   ДИ = [{ci_unknown_scipy[0]:.6f}, {ci_unknown_scipy[1]:.6f}], длина = {ci_unknown_scipy[1] - ci_unknown_scipy[0]:.6f}")

# -----------------------
# 1.3 Интервал для дисперсии
# -----------------------
print("\n1.3 ДИ для дисперсии σ²")

chi2_lower = stats.chi2.ppf((1 - gamma) / 2, df=n - 1)
chi2_upper = stats.chi2.ppf((1 + gamma) / 2, df=n - 1)

ci_var = ((n - 1) * s2 / chi2_upper, (n - 1) * s2 / chi2_lower)

print(f"Квантили распределения хи-квадрат:")
print(f"χ²_((1-gamma)/2) = χ²_({(1 - gamma) / 2:.6f}) = {chi2_lower:.6f}")
print(f"χ²_((1+gamma)/2) = χ²_({(1 + gamma) / 2:.6f}) = {chi2_upper:.6f}")
print(f"ДИ для σ² = [{ci_var[0]:.6f}, {ci_var[1]:.6f}], длина = {ci_var[1] - ci_var[0]:.6f}")
print(f"Покрывает ли интервал истинное σ² = {sigma2}? -> {ci_var[0] <= sigma2 <= ci_var[1]}")

# -----------------------
# 2. График длины ДИ в зависимости от надежности gamma (фиксирован n)
# -----------------------
gammas = np.linspace(0.50, 0.999, 60)
length_mean_known = []
length_mean_unknown = []
length_var = []

for g in gammas:
    z_g = stats.norm.ppf((1 + g) / 2)
    length_mean_known.append(2 * z_g * sigma / np.sqrt(n))
    t_g = stats.t.ppf((1 + g) / 2, df=n - 1)
    length_mean_unknown.append(2 * t_g * s / np.sqrt(n))
    # длина интервала для дисперсии
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

# -----------------------
# 3. График длины ДИ в зависимости от n (фиксирован gamma)
# -----------------------
ns = np.arange(10, 201, 5)
len_mean_known_n = []
len_mean_unknown_n = []
len_var_n = []

for n_val in ns:
    z_g = stats.norm.ppf((1 + gamma) / 2)
    len_mean_known_n.append(2 * z_g * sigma / np.sqrt(n_val))
    t_val = stats.t.ppf((1 + gamma) / 2, df=n_val - 1)
    len_mean_unknown_n.append(2 * t_val * s / np.sqrt(n_val))
    # длина для дисперсии
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

# -----------------------
# 4. Моделирование M выборок и оценка надежности gamma* для матожидания (σ неизвестна)
# -----------------------
print("\n4. Моделирование M выборок для оценки gamma* (для матожидания, σ неизвестна)")
cover_count = 0
for i in range(M):
    samp = np.random.normal(loc=a, scale=sigma, size=n)
    xb = np.mean(samp)
    s2m = np.var(samp, ddof=1)
    s_m = np.sqrt(s2m)
    tcrit = stats.t.ppf((1 + gamma) / 2, df=n - 1)
    low = xb - tcrit * s_m / np.sqrt(n)
    high = xb + tcrit * s_m / np.sqrt(n)
    if low <= a <= high:
        cover_count += 1

gamma_star = cover_count / M
print(f"M = {M}, число покрытий = {cover_count}, оценка gamma* = {gamma_star:.6f}")
print(f"Истинное gamma = {gamma}, отклонение = {abs(gamma_star - gamma):.6f}")

# -----------------------
# ОТВЕТЫ НА ВОПРОСЫ
# -----------------------
print("\n" + "=" * 70)
print("ОТВЕТЫ НА ВОПРОСЫ")
print("=" * 70)

# Вопрос 1: Надежность gamma для отклонения ≤ 0.25S
print("\n--- ВОПРОС 1 ---")
print("Какая надежность gamma гарантирует отклонение |x̄ - a| ≤ 0.25S?")
print(f"Условие: |x̄ - a| ≤ 0.25S, n = {n}")

t_needed = 0.25 * np.sqrt(n)
gamma_needed = 2 * stats.t.cdf(t_needed, df=n - 1) - 1

print(f"Решение:")
print(f"  t = 0.25 × √{n} = {t_needed:.4f}")
print(f"  gamma = 2 × F(t, {n - 1}) - 1 = {gamma_needed:.6f}")
print(f"ОТВЕТ: gamma ≈ {gamma_needed:.4f} ({gamma_needed * 100:.1f}%)")

# Вопрос 2: Объем выборки n для отклонения ≤ 0.25S при gamma=0.925
print("\n--- ВОПРОС 2 ---")
print("Какой объем выборки n гарантирует отклонение |x̄ - a| ≤ 0.25S?")
print(f"Условие: |x̄ - a| ≤ 0.25S, gamma = {gamma}")


# Быстрый поиск оптимального n
def find_n_quick(target_gamma=0.925, delta=0.25):
    best_n = n
    best_diff = float('inf')
    for n_candidate in range(10, 200):
        df = n_candidate - 1
        t_crit = stats.t.ppf((1 + target_gamma) / 2, df)
        right_side = delta * np.sqrt(n_candidate)
        diff = abs(t_crit - right_side)

        if diff < best_diff:
            best_diff = diff
            best_n = n_candidate

    return best_n, best_diff


n_required, error = find_n_quick(gamma, 0.25)
print(f"ОТВЕТ: n ≈ {n_required}")

# Вопросы 3-5
print("\n--- ВОПРОСЫ 3-5 ---")
print("3) Закон распределения точечной оценки gamma*: биномиальный")
print("   gamma* ~ Bin(M, gamma)/M, приближенно N(gamma, gamma(1-gamma)/M)")

# 95%-ый доверительный интервал для параметра γ
z_95 = stats.norm.ppf(0.975)
ci_gamma = (gamma_star - z_95 * np.sqrt(gamma_star * (1 - gamma_star) / M),
            gamma_star + z_95 * np.sqrt(gamma_star * (1 - gamma_star) / M))

print(f"4) 95% ДИ для параметра gamma: [{ci_gamma[0]:.6f}, {ci_gamma[1]:.6f}]")
print(f"   Накрыл ли построенный ДИ параметр gamma? -> {ci_gamma[0] <= gamma <= ci_gamma[1]}")

print(f"5) E[gamma*] = gamma = {gamma}")
print(f"   Var(gamma*) = gamma(1-gamma)/M = {gamma * (1 - gamma) / M:.8e}")

print("\nКонец работы.")