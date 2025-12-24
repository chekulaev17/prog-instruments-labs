import re

# -------- CONFIG -------- #
DEFAULT_VARIANT = 79
DEFAULT_FILE_PATH = "79.csv"
FILE_ENCODING = "utf-16"
CSV_DELIMITER = ";"


# -------- REGEX PATTERNS -------- #
# Исправленные регулярные выражения согласно форматам ЛР
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
HEIGHT_PATTERN = r'^\d\.\d{2}$'  # Формат: цифра.две цифры (например: 1.75)
INN_PATTERN = r'^\d{12}$'  # Ровно 12 цифр
PASSPORT_PATTERN = r'^\d{2}\s\d{2}\s\d{6}$'  # 2 цифры, пробел, 2 цифры, пробел, 6 цифр
OCCUPATION_PATTERN = r'^[A-Za-zА-Яа-яЁё\s\-\.\(\)/]+$'  # Буквы, пробелы, дефисы, точки, скобки, слэши
LATITUDE_PATTERN = r'^-?(?:90(?:\.0+)?|[0-8]?\d(?:\.\d+)?)$'  # Широта от -90.0 до +90.0
HEX_COLOR_PATTERN = r'^#[0-9a-fA-F]{6}$'  # HEX цвет с #
ISSN_PATTERN = r'^\d{4}-\d{4}$'  # ISSN: XXXX-XXXX
UUID_PATTERN = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'  # UUID
# Время: HH:MM:SS.ffffff (микросекунды обязательно 6 цифр)
TIME_PATTERN = r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)\.\d{6}$'

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
    return [re.compile(pattern, re.IGNORECASE) for pattern in PATTERNS]