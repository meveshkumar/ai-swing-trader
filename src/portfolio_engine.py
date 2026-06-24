from scoring_engine import ScoringEngine


class PortfolioEngine:

    def __init__(self):
        self.scoring_engine = ScoringEngine()

        self.portfolio = [
            {
                "symbol": "RELIANCE.NS",
                "quantity": 10,
                "entry_price": 1200
            },
            {
                "symbol": "TCS.NS",
                "quantity": 5,
                "entry_price": 3500
            },
            {
                "symbol": "INFY.NS",
                "quantity": 8,
                "entry_price": 1500
            }
        ]

    def analyze_portfolio(self):

        results = []

        for stock in self.portfolio:

            symbol = stock["symbol"]
            quantity = stock["quantity"]
            entry_price = stock["entry_price"]

            df = self.scoring_engine.analyze_symbol(
                symbol
            )

            if df.empty:
                continue

            latest = df.iloc[-1]

            current_price = float(
                latest["Close"]
            )

            investment = (
                quantity * entry_price
            )

            current_value = (
                quantity * current_price
            )

            profit_loss = (
                current_value - investment
            )

            profit_loss_pct = (
                (profit_loss / investment)
                * 100
            )

            results.append(
                {
                    "Symbol": symbol,
                    "Quantity": quantity,
                    "Entry Price": round(
                        entry_price,
                        2
                    ),
                    "Current Price": round(
                        current_price,
                        2
                    ),
                    "Investment": round(
                        investment,
                        2
                    ),
                    "Current Value": round(
                        current_value,
                        2
                    ),
                    "Profit/Loss": round(
                        profit_loss,
                        2
                    ),
                    "Profit/Loss %": round(
                        profit_loss_pct,
                        2
                    ),
                    "Signal": latest["SIGNAL"],
                    "Score": int(
                        latest["SCORE"]
                    ),
                    "Rating": latest["RATING"]
                }
            )

        return results

    def portfolio_summary(
        self,
        portfolio_data
    ):

        total_investment = sum(
            item["Investment"]
            for item in portfolio_data
        )

        total_current_value = sum(
            item["Current Value"]
            for item in portfolio_data
        )

        total_profit_loss = (
            total_current_value
            - total_investment
        )

        return {
            "Total Investment":
                round(
                    total_investment,
                    2
                ),

            "Total Current Value":
                round(
                    total_current_value,
                    2
                ),

            "Total Profit/Loss":
                round(
                    total_profit_loss,
                    2
                )
        }


if __name__ == "__main__":

    engine = PortfolioEngine()

    portfolio = (
        engine.analyze_portfolio()
    )

    print("\nPortfolio Analysis\n")

    for stock in portfolio:

        print(stock)

    summary = (
        engine.portfolio_summary(
            portfolio
        )
    )

    print("\nPortfolio Summary\n")

    print(summary)