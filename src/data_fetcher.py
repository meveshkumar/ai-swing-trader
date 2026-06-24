"""
==================================================
AI Swing Trader - Data Fetcher Module
Version: 1.0.0
==================================================
"""

import logging

import pandas as pd
import yfinance as yf

import settings
from database import DatabaseManager


class DataFetcher:
    """
    Downloads historical stock data from Yahoo Finance
    and stores it in the SQLite database.
    """

    def __init__(self):
        self.db = DatabaseManager()

    def download_stock_data(self, symbol):
        """
        Download historical data for one stock.
        """

        logging.info(f"Downloading data for {symbol}")

        try:

            dataframe = yf.download(
                tickers=symbol,
                period=settings.DOWNLOAD_PERIOD,
                interval=settings.DOWNLOAD_INTERVAL,
                auto_adjust=settings.AUTO_ADJUST,
                progress=settings.SHOW_PROGRESS,
            )

            if dataframe.empty:
                logging.warning(f"No data found for {symbol}")

            return dataframe

        except Exception as error:

            logging.error(
                f"Download failed for {symbol}: {error}"
            )

            return pd.DataFrame()

    def clean_dataframe(self, dataframe):
        """
        Clean downloaded dataframe before saving.
        """

        if dataframe.empty:
            return dataframe

        dataframe = dataframe.copy()

        # Handle Yahoo Finance MultiIndex columns
        if isinstance(dataframe.columns, pd.MultiIndex):
            dataframe.columns = dataframe.columns.get_level_values(0)

        dataframe.reset_index(inplace=True)

        dataframe.drop_duplicates(inplace=True)

        dataframe.dropna(inplace=True)

        return dataframe

    def save_dataframe(self, symbol, dataframe):
        """
        Save dataframe into SQLite database.
        """

        if dataframe.empty:
            return

        required_columns = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        for _, row in dataframe.iterrows():

            if "Adj Close" in dataframe.columns:
                adj_close = float(row["Adj Close"])
            else:
                adj_close = float(row["Close"])

            date_value = row["Date"]

            if hasattr(date_value, "strftime"):
                date_value = date_value.strftime("%Y-%m-%d")
            else:
                date_value = str(date_value)

            self.db.insert_stock_data(
                date=date_value,
                symbol=symbol,
                open_price=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                adj_close=adj_close,
                volume=int(row["Volume"]),
            )

    def fetch_single_stock(self, symbol):
        """
        Download, clean and save one stock.
        """

        try:

            dataframe = self.download_stock_data(symbol)

            if dataframe.empty:
                return False

            dataframe = self.clean_dataframe(dataframe)

            self.save_dataframe(symbol, dataframe)

            logging.info(
                f"{symbol} downloaded and saved successfully."
            )

            return True

        except Exception as error:

            logging.exception(
                f"Failed to process {symbol}: {error}"
            )

            return False

    def run_data_collection(self, stock_list):
        """
        Download data for multiple stocks.
        """

        success = 0
        failed = 0

        logging.info(
            "Starting market data collection..."
        )

        for symbol in stock_list:

            if self.fetch_single_stock(symbol):
                success += 1
            else:
                failed += 1

        logging.info(
            f"Completed | Success: {success} | Failed: {failed}"
        )

        return success, failed