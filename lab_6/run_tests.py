#!/usr/bin/env python3
"""
Скрипт для запуска всех unit-тестов с выводом в консоль.
"""
import subprocess
import sys
import os


def print_header():
    """Вывод заголовка тестирования."""
    print("\n" + "=" * 70)
    print("UNIT-ТЕСТЫ ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ ПО СТАТИСТИКЕ")
    print("=" * 70)


def run_tests():
    """Запуск всех тестов через pytest."""
    print_header()

    # Команда для запуска pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",  # Подробный вывод
        "--tb=short",  # Короткий traceback
        "--disable-warnings",  # Отключить предупреждения
    ]

    print(f"\nЗапуск команды: {' '.join(cmd)}")
    print("-" * 70)

    # Запускаем тесты
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    # Выводим результаты
    print(result.stdout)

    if result.stderr:
        print("\nОШИБКИ И ПРЕДУПРЕЖДЕНИЯ:")
        print("-" * 70)
        print(result.stderr)

    # Анализируем вывод для статистики
    lines = result.stdout.split('\n')
    passed = 0
    failed = 0
    skipped = 0

    for line in lines:
        if "passed" in line and "failed" in line and "skipped" in line:
            # Извлекаем статистику из строки вида:
            # 7 passed, 2 failed, 1 skipped in 0.12s
            parts = line.split()
            for part in parts:
                if part.endswith('passed'):
                    passed = int(part.replace('passed', ''))
                elif part.endswith('failed'):
                    failed = int(part.replace('failed', ''))
                elif part.endswith('skipped'):
                    skipped = int(part.replace('skipped', ''))

    # Выводим итоговую статистику
    print("\n" + "=" * 70)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    print(f"✅ Пройдено: {passed}")
    print(f"❌ Не пройдено: {failed}")
    print(f"⏩ Пропущено: {skipped}")

    total = passed + failed + skipped
    if total > 0:
        success_rate = (passed / total) * 100
        print(f"\n📊 Успешность: {success_rate:.1f}%")

    if failed == 0:
        print("\n🎉 ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
    else:
        print(f"\n⚠️  Найдено {failed} ошибок в тестах")

    print("=" * 70)

    return result.returncode


if __name__ == "__main__":
    # Проверяем наличие pytest
    try:
        import pytest
    except ImportError:
        print("❌ Ошибка: pytest не установлен!")
        print("   Установите его: pip install pytest")
        sys.exit(1)

    # Проверяем наличие тестов
    if not os.path.exists("tests"):
        print("❌ Ошибка: папка tests не найдена!")
        sys.exit(1)

    # Запускаем тесты
    exit_code = run_tests()
    sys.exit(exit_code)