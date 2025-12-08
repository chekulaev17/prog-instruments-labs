import json
import hashlib
from typing import List

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    ВНИМАНИЕ, ВАЖНО! Чтобы сумма получилась корректной, считать, что первая строка с данными csv-файла имеет номер 0.
    В исходном csv 1я строка - заголовки, 2я - первая строка данных, т.е. номер 0.

    :param row_numbers: список номеров строк, на которых найдены ошибки
    :return: md5 хеш
    """
    row_numbers.sort()
    return hashlib.md5(
        json.dumps(row_numbers).encode("utf-8")
    ).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Создаёт файл result.json со структурой:
    {
        "variant": <номер>,
        "checksum": "<md5>"
    }

    :param variant: номер варианта
    :param checksum: контрольная сумма
    """
    result = {
        "variant": variant,
        "checksum": checksum
    }

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(calculate_checksum([1, 2, 3]))
    print(calculate_checksum([3, 2, 1]))
