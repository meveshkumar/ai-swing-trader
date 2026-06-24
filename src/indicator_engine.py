import sqlite3
import pandas as pd

from settings import DATABASE_FILE


class IndicatorEngine:

    def __init__(self):
        self.db_path = DATABASE_FILE

    def load_data(self, symbol):
        """
        Load historical data from SQLite database
        """

        conn = sqlite3.connect(self.db_path)

        query = """
        SELECT *
        FROM market_data
        WHERE Symbol = ?
        ORDER BY Date
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(symbol,)
        )

        conn.close()

        return df

    def calculate_sma(self, df, period):
        """
        Calculate Simple Moving Average
        """

        return (
            df["Close"]
            .rolling(window=period)
            .mean()
        )

    def calculate_ema(self, df, period):
        """
        Calculate Exponential Moving Average
        """

        return (
            df["Close"]
            .ewm(
                span=period,
                adjust=False
            )
            .mean()
        )

    def calculate_rsi(self, df, period=14):
        """
        Calculate Relative Strength Index (RSI)
        """

        delta = df["Close"].diff()

        gain = delta.where(
            delta > 0,
            0
        )

        loss = -delta.where(
            delta < 0,
            0
        )

        avg_gain = gain.rolling(
            window=period
        ).mean()

        avg_loss = loss.rolling(
            window=period
        ).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (
            100 / (1 + rs)
        )

        return rsi

    def calculate_macd(self, df):
        """
        Calculate MACD
        """

        ema12 = (
            df["Close"]
            .ewm(
                span=12,
                adjust=False
            )
            .mean()
        )

        ema26 = (
            df["Close"]
            .ewm(
                span=26,
                adjust=False
            )
            .mean()
        )

        macd = ema12 - ema26

        signal = (
            macd
            .ewm(
                span=9,
                adjust=False
            )
            .mean()
        )

        histogram = macd - signal

        return macd, signal, histogram

    def calculate_average_volume(
        self,
        df,
        period=20
    ):
        """
        Calculate Average Volume
        """

        return (
            df["Volume"]
            .rolling(window=period)
            .mean()
        )

    def calculate_indicators(
        self,
        symbol
    ):
        """
        Calculate all indicators
        """

        df = self.load_data(symbol)

        if df.empty:
            return df

        df["SMA_20"] = self.calculate_sma(
            df,
            20
        )

        df["SMA_50"] = self.calculate_sma(
            df,
            50
        )

        df["EMA_20"] = self.calculate_ema(
            df,
            20
        )

        df["RSI_14"] = self.calculate_rsi(
            df,
            14
        )

        macd, signal, histogram = (
            self.calculate_macd(df)
        )

        df["MACD"] = macd
        df["MACD_SIGNAL"] = signal
        df["MACD_HISTOGRAM"] = histogram

        df["AVG_VOLUME_20"] = (
            self.calculate_average_volume(
                df,
                20
            )
        )

        return df


if __name__ == "__main__":

    engine = IndicatorEngine()

    df = engine.calculate_indicators(
        "RELIANCE.NS"
    )

    print("\nLast 10 Records\n")

    print(
        df[
            [
                "Date",
                "Close",
                "SMA_20",
                "SMA_50",
                "EMA_20",
                "RSI_14",
                "MACD",
                "MACD_SIGNAL",
                "MACD_HISTOGRAM",
                "AVG_VOLUME_20"
            ]
        ].tail(10)
    )