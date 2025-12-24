import re

# -------- CONFIG -------- #
DEFAULT_VARIANT = 79
DEFAULT_FILE_PATH = "79.csv"
FILE_ENCODING = "utf-16"
CSV_DELIMITER = ";"

# -------- REGEX PATTERNS -------- #
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
HEIGHT_PATTERN = r'^[12]\.\d{1,5}$'
INN_PATTERN = r'^\d{12}$'
PASSPORT_PATTERN = r'^\d{2}\s\d{2}\s\d{6}$'
OCCUPATION_PATTERN = r'^[А-Яа-яA-Za-z\s\-\./,\(\)]+$'
LATITUDE_PATTERN = r'^-?\d{1,2}\.\d+$'
HEX_COLOR_PATTERN = r'^#[0-9A-Fa-f]{6}$'
ISSN_PATTERN = r'^\d{4}-\d{4}$'
UUID_PATTERN = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
TIME_PATTERN = r'^\d{2}:\d{2}:\d{2}(\.\d+)?$'

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