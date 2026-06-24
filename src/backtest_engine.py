"""
==================================================
AI Swing Trader - Backtesting Engine
Version: 1.5.0
==================================================
"""

from signal_engine import SignalEngine


class BacktestEngine:
    """
    Simulate historical BUY and SELL trades
    and calculate strategy performance.
    """

    def __init__(self):
        self.signal_engine = SignalEngine()

    def analyze_symbol(self, symbol):
        """
        Run backtest for one stock.
        """

        df = self.signal_engine.analyze_symbol(
            symbol
        )

        if df.empty:
            return {}

        position_open = False

        buy_price = 0.0

        total_trades = 0

        winning_trades = 0

        losing_trades = 0

        total_profit_percent = 0.0

        for _, row in df.iterrows():

            signal = row["SIGNAL"]

            close_price = float(
                row["Close"]
            )

            # BUY

            if (
                signal == "BUY"
                and not position_open
            ):

                buy_price = close_price

                position_open = True

            # SELL

            elif (
                signal == "SELL"
                and position_open
            ):

                sell_price = close_price

                profit_percent = (
                    (
                        sell_price
                        - buy_price
                    )
                    / buy_price
                ) * 100

                total_profit_percent += (
                    profit_percent
                )

                total_trades += 1

                if profit_percent > 0:

                    winning_trades += 1

                else:

                    losing_trades += 1

                position_open = False

        # Win Rate

        if total_trades > 0:

            win_rate = (
                winning_trades
                / total_trades
            ) * 100

        else:

            win_rate = 0

        results = {

            "Symbol": symbol,

            "Total Trades":
                total_trades,

            "Winning Trades":
                winning_trades,

            "Losing Trades":
                losing_trades,

            "Win Rate (%)":
                round(
                    win_rate,
                    2
                ),

            "Profit/Loss (%)":
                round(
                    total_profit_percent,
                    2
                )
        }

        return results


if __name__ == "__main__":

    engine = BacktestEngine()

    results = engine.analyze_symbol(
        "RELIANCE.NS"
    )

    print("\nBacktest Results\n")

    for key, value in results.items():

        print(
            f"{key}: {value}"
        )