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