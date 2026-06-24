"""
==================================================
AI Swing Trader - Settings
Version: 1.0.0
==================================================
"""

# ==================================================
# Project Information
# ==================================================

PROJECT_NAME = "AI Swing Trader"
VERSION = "1.0.0"

# ==================================================
# Data Provider
# ==================================================

DATA_PROVIDER = "Yahoo Finance"

# ==================================================
# Market Configuration
# ==================================================

MARKET = "NSE"
INDEX_NAME = "NIFTY 500"

# ==================================================
# Historical Data Download Settings
# ==================================================

# For testing use "1mo"
# Later change to "max"

DOWNLOAD_PERIOD = "1mo"

# Valid values:
# 1d, 5d, 1wk, 1mo, 3mo

DOWNLOAD_INTERVAL = "1d"

# ==================================================
# Analysis Settings
# ==================================================

DAILY_LOOKBACK_DAYS = 365

WEEKLY_LOOKBACK_YEARS = 5

BACKTEST_HISTORY = "max"

# ==================================================
# Folder Structure
# ==================================================

DATA_FOLDER = "../data"

REPORT_FOLDER = "../reports"

LOG_FOLDER = "../logs"

# ==================================================
# Files
# ==================================================

NIFTY500_FILE = f"{DATA_FOLDER}/nifty500.csv"

DATABASE_FILE = f"{DATA_FOLDER}/market_data.db"

LOG_FILE = f"{LOG_FOLDER}/application.log"

EXCEL_REPORT = (
    f"{REPORT_FOLDER}/AI_Swing_Trader_Report.xlsx"
)

# ==================================================
# Logging
# ==================================================

LOG_LEVEL = "INFO"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(message)s"
)

# ==================================================
# Yahoo Finance
# ==================================================

AUTO_ADJUST = False

SHOW_PROGRESS = False