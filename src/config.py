"""
===========================================================
AI Swing Trader
Configuration File
===========================================================
"""

# ==========================
# Project Information
# ==========================

PROJECT_NAME = "AI Swing Trader"
VERSION = "1.2.0"

# ==========================
# Market Configuration
# ==========================

MARKET = "NSE"
INDEX_NAME = "NIFTY 500"

# ==========================
# Folder Paths
# ==========================

DATA_FOLDER = "data"
REPORTS_FOLDER = "reports"
LOGS_FOLDER = "logs"

# ==========================
# Output Files
# ==========================

STOCK_LIST_FILE = f"{DATA_FOLDER}/nifty500.csv"
PRICE_DATA_FILE = f"{DATA_FOLDER}/price_data.csv"

# ==========================
# Analysis Settings
# ==========================

# Historical Data

DOWNLOAD_PERIOD = "max"

# Daily Analysis

DAILY_LOOKBACK = 365

# Weekly Deep Analysis

WEEKLY_LOOKBACK = 5

# Backtesting

BACKTEST_MIN_HISTORY = 5

# ==========================
# Logging
# ==========================

LOG_FILE = f"{LOGS_FOLDER}/application.log"