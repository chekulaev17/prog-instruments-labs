import csv
import re
from checksum import calculate_checksum, serialize_result
from consts import (
    DEFAULT_VARIANT,
    DEFAULT_FILE_PATH,
    FILE_ENCODING,
    CSV_DELIMITER,
    get_validation_patterns,
)


def load_data(
        file_path: str, delimiter: str = CSV_DELIMITER
) -> list[list[str]]:
    """
    Загружает CSV-файл и возвращает список строк,
    каждая строка представлена списком ячеек.
    """
    with open(
            file_path, "r", encoding=FILE_ENCODING, newline=""
    ) as file:
        reader = csv.reader(file, delimiter=delimiter)
        return list(reader)


def validate_row(row: list[str], patterns: list[re.Pattern]) -> bool:
    """
    Проверяет строку CSV.
    Количество значений должно совпадать с количеством паттернов.
    Каждая ячейка должна проходить pattern.fullmatch.

    Дополнительные проверки для специфичных форматов.
    """
    if len(row) != len(patterns):
        return False

    for pattern, value in zip(patterns, row):
        value_stripped = value.strip()

        # Проверка регулярным выражением
        if not pattern.fullmatch(value_stripped):
            return False

        # Дополнительные проверки для специфичных форматов

        # Проверка высоты (должна быть от 0.5 до 2.5 метров)
        if pattern.pattern == r'^\d\.\d{2}$':
            try:
                height = float(value_stripped)
                if height < 0.5 or height > 2.5:
                    return False
            except ValueError:
                return False

        # Проверка широты (должна быть от -90 до +90)
        elif pattern.pattern == r'^-?(?:90(?:\.0+)?|[0-8]?\d(?:\.\d+)?)$':
            try:
                lat = float(value_stripped)
                if lat < -90.0 or lat > 90.0:
                    return False
            except ValueError:
                return False

        # Проверка времени (дополнительная проверка микросекунд)
        elif pattern.pattern == r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)\.\d{6}$':
            if '.' in value_stripped:
                time_part, micro_part = value_stripped.split('.')
                if len(micro_part) != 6:
                    return False

    return True


def find_invalid_rows(
        data: list[list[str]], patterns: list[re.Pattern]
) -> list[int]:
    """
    Возвращает список индексов невалидных строк.
    Индексация соответствует требованиям checksum-модуля.
    """
    invalid = []

    # Пропускаем заголовок: data[1:]
    for index, row in enumerate(data[1:], start=0):
        if not validate_row(row, patterns):
            invalid.append(index)

    return invalid


def main() -> None:
    """
    Основной запуск:
    - загрузка данных
    - валидация
    - вычисление контрольной суммы
    - запись в result.json
    """
    print("=== CSV Validation Script ===")
    print(f"Валидация файла: {DEFAULT_FILE_PATH}")
    print(f"Вариант: {DEFAULT_VARIANT}")

    try:
        data = load_data(DEFAULT_FILE_PATH)
        print(f"Загружено строк: {len(data)}")
        print(f"Заголовки: {data[0] if data else 'нет данных'}")

        patterns = get_validation_patterns()
        print(f"Количество паттернов: {len(patterns)}")

        invalid_rows = find_invalid_rows(data, patterns)

        print(f"Невалидных строк: {len(invalid_rows)}")
        print(f"Всего строк данных: {len(data) - 1}")

        checksum_value = calculate_checksum(invalid_rows)
        serialize_result(DEFAULT_VARIANT, checksum_value)

        print(f"Контрольная сумма: {checksum_value}")
        print(f"Результат записан в result.json (вариант {DEFAULT_VARIANT})")

    except FileNotFoundError:
        print(f"Ошибка: Файл {DEFAULT_FILE_PATH} не найден!")
    except Exception as e:
        print(f"Ошибка при выполнении: {str(e)}")


if __name__ == "__main__":
    main()