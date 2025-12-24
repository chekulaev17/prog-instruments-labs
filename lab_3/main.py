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
    """
    if len(row) != len(patterns):
        return False

    for pattern, value in zip(patterns, row):
        if not pattern.fullmatch(value.strip()):
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

    data = load_data(DEFAULT_FILE_PATH)
    patterns = get_validation_patterns()
    invalid_rows = find_invalid_rows(data, patterns)

    print(f"Невалидных строк: {len(invalid_rows)}")

    checksum_value = calculate_checksum(invalid_rows)
    serialize_result(DEFAULT_VARIANT, checksum_value)

    print(f"Контрольная сумма: {checksum_value}")
    print(
        f"Результат записан в result.json "
        f"(вариант {DEFAULT_VARIANT})"
    )


if __name__ == "__main__":
    main()