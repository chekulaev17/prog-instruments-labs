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