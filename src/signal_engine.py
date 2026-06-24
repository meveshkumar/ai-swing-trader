from indicator_engine import IndicatorEngine


class SignalEngine:

    def __init__(self):
        self.indicator_engine = IndicatorEngine()

    def generate_signal(self, row):
        """
        Generate trading signal
        """

        sma_bullish = (
            row["SMA_20"] > row["SMA_50"]
        )

        sma_bearish = (
            row["SMA_20"] < row["SMA_50"]
        )

        rsi_bullish = (
            row["RSI_14"] > 50
        )

        rsi_bearish = (
            row["RSI_14"] < 50
        )

        macd_bullish = (
            row["MACD"] >
            row["MACD_SIGNAL"]
        )

        macd_bearish = (
            row["MACD"] <
            row["MACD_SIGNAL"]
        )

        if (
            sma_bullish
            and rsi_bullish
            and macd_bullish
        ):
            return "BUY"

        if (
            sma_bearish
            and rsi_bearish
            and macd_bearish
        ):
            return "SELL"

        return "HOLD"

    def analyze_symbol(
        self,
        symbol
    ):
        """
        Analyze one stock
        """

        df = (
            self.indicator_engine
            .calculate_indicators(symbol)
        )

        if df.empty:
            return df

        df["SIGNAL"] = (
            df.apply(
                self.generate_signal,
                axis=1
            )
        )

        return df


if __name__ == "__main__":

    engine = SignalEngine()

    df = engine.analyze_symbol(
        "RELIANCE.NS"
    )

    print("\nLatest Analysis\n")

    print(
        df[
            [
                "Date",
                "Close",
                "SMA_20",
                "SMA_50",
                "RSI_14",
                "MACD",
                "MACD_SIGNAL",
                "SIGNAL"
            ]
        ].tail(10)
    )

    
    print("\nLatest Signal:\n")

    print(
        df.iloc[-1]["SIGNAL"]
    )