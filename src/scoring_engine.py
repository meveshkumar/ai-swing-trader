from signal_engine import SignalEngine


class ScoringEngine:

    def __init__(self):
        self.signal_engine = SignalEngine()

    def calculate_score(self, row):
        """
        Calculate stock score
        """

        score = 0

        # SMA Score

        if row["SMA_20"] > row["SMA_50"]:
            score += 30

        # RSI Score

        if row["RSI_14"] > 60:
            score += 25

        elif row["RSI_14"] >= 50:
            score += 15

        else:
            score += 5

        # MACD Score

        if row["MACD"] > row["MACD_SIGNAL"]:
            score += 25

        else:
            score += 5

        # Signal Score

        if row["SIGNAL"] == "BUY":
            score += 20

        elif row["SIGNAL"] == "HOLD":
            score += 10

        return score

    def get_rating(self, score):
        """
        Convert score to rating
        """

        if score >= 90:
            return "STRONG BUY"

        elif score >= 70:
            return "BUY"

        elif score >= 40:
            return "HOLD"

        return "SELL"

    def analyze_symbol(self, symbol):
        """
        Analyze one stock and assign score
        """

        df = self.signal_engine.analyze_symbol(
            symbol
        )

        if df.empty:
            return df

        df["SCORE"] = (
            df.apply(
                self.calculate_score,
                axis=1
            )
        )

        df["RATING"] = (
            df["SCORE"]
            .apply(self.get_rating)
        )

        return df


if __name__ == "__main__":

    engine = ScoringEngine()

    df = engine.analyze_symbol(
        "RELIANCE.NS"
    )

    print("\nLatest Analysis\n")

    print(
        df[
            [
                "Date",
                "Close",
                "SIGNAL",
                "SCORE",
                "RATING"
            ]
        ].tail(10)
    )

    print("\nLatest Stock Rating\n")

    latest = df.iloc[-1]

    print(
        f"Signal : {latest['SIGNAL']}"
    )

    print(
        f"Score  : {latest['SCORE']}"
    )

    print(
        f"Rating : {latest['RATING']}"
    )