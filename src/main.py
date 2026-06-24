"""
==================================================
AI Swing Trader - Main Module
Version: 1.0.0
==================================================
"""

import logging
import os

import settings
from database import DatabaseManager
from data_fetcher import DataFetcher


def setup_logging():
    """
    Configure application logging.
    """

    os.makedirs(settings.LOG_FOLDER, exist_ok=True)

    logging.basicConfig(
        filename=settings.LOG_FILE,
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        filemode="a",
    )


def main():
    """
    Main application entry point.
    """

    print("=" * 60)
    print(settings.PROJECT_NAME)
    print(f"Version : {settings.VERSION}")
    print("=" * 60)

    # Configure logging
    setup_logging()

    logging.info("Application started.")

    # Initialize database
    db = DatabaseManager()
    db.create_database()

    # Create data fetcher
    fetcher = DataFetcher()

    # Version 1.0 Test Stock
    stock_list = [
        "RELIANCE.NS",
    ]

    success, failed = fetcher.run_data_collection(stock_list)

    print()
    print("=" * 60)
    print("Data Collection Completed")
    print("=" * 60)
    print(f"Successful Downloads : {success}")
    print(f"Failed Downloads     : {failed}")
    print("=" * 60)

    logging.info("Application finished successfully.")


if __name__ == "__main__":
    main()