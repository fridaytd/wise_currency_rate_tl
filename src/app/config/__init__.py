import os
from typing import Final

# Logger
LOG_NAME: Final[str] = os.environ["LOG_NAME"]
LOG_LEVEL: Final[str] = os.environ["LOG_LEVEL"]
IS_LOG_FILE: Final[str] = os.environ["IS_LOG_FILE"]
LOG_FILE_NAME: Final[str] = os.environ["LOG_FILE_NAME"]

# Keys
KEYS_PATH: Final[str] = os.environ["KEYS_PATH"]

# Sheets
SPREADSHEET_KEY: Final[str] = os.environ["SPREADSHEET_KEY"]
SHEET_NAME: Final[str] = os.environ["SHEET_NAME"]

# Wise api key
WISE_API_KEY: Final[str] = os.environ["WISE_API_KEY"]


# Relax time each round in second
RELAX_TIME_EACH_ROUND: Final[str] = os.environ["RELAX_TIME_EACH_ROUND"]


START_INDEX: Final[int] = 4
END_INDEX: Final[int] = 25761
