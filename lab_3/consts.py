import re

# -------- CONFIG -------- #
DEFAULT_VARIANT = 79
DEFAULT_FILE_PATH = "79.csv"
FILE_ENCODING = "utf-16"
CSV_DELIMITER = ";"


# -------- REGEX PATTERNS (замени своими!) -------- #
EMAIL_PATTERN = r".+"
HEIGHT_PATTERN = r".+"
INN_PATTERN = r".+"
PASSPORT_PATTERN = r".+"
OCCUPATION_PATTERN = r".+"
LATITUDE_PATTERN = r".+"
HEX_COLOR_PATTERN = r".+"
ISSN_PATTERN = r".+"
UUID_PATTERN = r".+"
TIME_PATTERN = r".+"

PATTERNS = [
    EMAIL_PATTERN,
    HEIGHT_PATTERN,
    INN_PATTERN,
    PASSPORT_PATTERN,
    OCCUPATION_PATTERN,
    LATITUDE_PATTERN,
    HEX_COLOR_PATTERN,
    ISSN_PATTERN,
    UUID_PATTERN,
    TIME_PATTERN,
]


def get_validation_patterns() -> list[re.Pattern]:
    """
    Возвращает список скомпилированных регулярных выражений.
    """
    return [re.compile(pattern) for pattern in PATTERNS]
