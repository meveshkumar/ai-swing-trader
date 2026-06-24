"""
==================================================
AI Swing Trader - Database Module
Version: 1.0.0
==================================================
"""

import os
import sqlite3

import settings


class DatabaseManager:
    """
    Handles all SQLite database operations.
    """

    def __init__(self):
        self.database = settings.DATABASE_FILE

    def get_connection(self):
        """
        Create and return a SQLite connection.
        """

        os.makedirs(os.path.dirname(self.database), exist_ok=True)

        return sqlite3.connect(self.database)

    def create_database(self):
        """
        Create all required database tables.
        """

        connection = self.get_connection()
        cursor = connection.cursor()

        # ==================================================
        # Historical Market Data
        # ==================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (

            Date TEXT NOT NULL,

            Symbol TEXT NOT NULL,

            Open REAL,

            High REAL,

            Low REAL,

            Close REAL,

            Adj_Close REAL,

            Volume INTEGER,

            PRIMARY KEY (Date, Symbol)

        )
        """)

        # ==================================================
        # Nifty 500 Stock List
        # ==================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nifty500 (

            Symbol TEXT PRIMARY KEY,

            Company TEXT,

            Industry TEXT

        )
        """)

        # ==================================================
        # Portfolio
        # ==================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (

            Symbol TEXT,

            Buy_Date TEXT,

            Buy_Price REAL,

            Quantity INTEGER,

            PRIMARY KEY (Symbol, Buy_Date)

        )
        """)

        # ==================================================
        # Daily Recommendations
        # ==================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (

            Date TEXT,

            Symbol TEXT,

            Technical_Score REAL,

            Market_Score REAL,

            Sector_Score REAL,

            News_Score REAL,

            Opportunity_Score REAL,

            Signal TEXT,

            PRIMARY KEY (Date, Symbol)

        )
        """)

        connection.commit()
        connection.close()

        print("✓ Database initialized successfully.")

    def insert_stock_data(
        self,
        date,
        symbol,
        open_price,
        high,
        low,
        close,
        adj_close,
        volume,
    ):
        """
        Insert one row of historical stock data.
        """

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO market_data
            (
                Date,
                Symbol,
                Open,
                High,
                Low,
                Close,
                Adj_Close,
                Volume
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date,
                symbol,
                open_price,
                high,
                low,
                close,
                adj_close,
                volume,
            ),
        )

        connection.commit()
        connection.close()

    def fetch_market_data(self, symbol):
        """
        Return all historical data for a stock.
        """

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM market_data
            WHERE Symbol = ?
            ORDER BY Date
            """,
            (symbol,),
        )

        rows = cursor.fetchall()

        connection.close()

        return rows

    def clear_market_data(self):
        """
        Delete all historical market data.
        """

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM market_data
            """
        )

        connection.commit()
        connection.close()

        print("✓ Market data cleared.")

    def close(self):
        """
        Placeholder for future compatibility.
        """

        pass