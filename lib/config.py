"""
Configuration settings for Atlanta Crime Map Dashboard (Streamlit version)
"""
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Primary data file (2021-2025 data)
LATEST_DATA_FILE = "AxonCrimeData_Export_view_6594257177302908045.csv"

# Historical data files
HISTORICAL_FILES = {
    "1997-2002": "Crime_Data_1997_2002.csv",
    "2003-2008": "Crime_Data_2003_2008.csv",
    "2009-2020": "2009_2020CrimeData_3002993194443433393.csv",
    "2021-2025": LATEST_DATA_FILE
}

# Severity crosswalk file
SEVERITY_CROSSWALK_FILE = "atl_ucr_nibrs_severity_crosswalk_full.csv"
SEVERITY_CROSSWALK_PATH = PROCESSED_DATA_DIR / SEVERITY_CROSSWALK_FILE

# Dashboard configuration
LOCATIONS = {
    "234 MEMORIAL DR SW": "The Welcome House",
    "277 MORELAND AVE SE": "Ralph David House"
}
DEFAULT_LOCATION = "234 MEMORIAL DR SW"
DEFAULT_DATE_RANGE = {
    "start": "2021-01-01",
    "end": "2025-12-31"
}

# Date parsing format for CSV files
DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"

# Display formats for UI consistency
DISPLAY_DATE_FORMAT = "%m/%d/%Y"
DISPLAY_DATETIME_FORMAT = "%m/%d/%Y %I:%M %p"

# Crime severity levels (for future implementation)
SEVERITY_LEVELS = {
    "HIGH": ["HOMICIDE", "RAPE", "ROBBERY", "AGG ASSAULT"],
    "MEDIUM": ["BURGLARY", "LARCENY", "MOTOR VEHICLE THEFT"],
    "LOW": ["SIMPLE ASSAULT", "VANDALISM", "DISORDERLY CONDUCT"]
}

# Time of day definitions
TIME_PERIODS = {
    "EARLY_MORNING": (0, 6),    # 12am - 6am
    "MORNING": (6, 12),          # 6am - 12pm
    "AFTERNOON": (12, 17),       # 12pm - 5pm
    "EVENING": (17, 21),         # 5pm - 9pm
    "NIGHT": (21, 24)            # 9pm - 12am
}

# Day/Night split (as used in current dashboard)
DAY_NIGHT_SPLIT = {
    "DAY": (5, 17),    # 5am - 5pm
    "NIGHT": (17, 5)   # 5pm - 5am (wraps around)
}