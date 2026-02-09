# stock_market_visual.py

import os
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from datetime import datetime

# ==========================================
# GET API KEYS FROM ENVIRONMENT VARIABLES
# ==========================================
API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

if not API_KEY or not API_SECRET:
    raise RuntimeError("Alpaca API keys not found. Set APCA_API_KEY_ID and APCA_API_SECRET_KEY.")

# Connect to Alpaca
api = tradeapi.REST(
    API_KEY,
    API_SECRET,
    BASE_URL,
    api_version="v2"
)

# ==========================================
# MOVING AVERAGE FUNCTION
# ==========================================
def moving_average(prices, days):
    return sum(prices[-days:]) / days


# ==========================================
# TRADING LOGIC (Golden Cross Strategy)
# ==========================================
def trade_decision(prices):
    if len(prices) < 200:
        return "NOT ENOUGH DATA"

    short_ma = moving_average(prices, 50)
    long_ma = moving_average(prices, 200)

    prev_short = moving_average(prices[:-1], 50)
    prev_long = moving_average(prices[:-1], 200)

    if prev_short <= prev_long and short_ma > long_ma:
        return "BUY"
    elif prev_short >= prev_long and short_ma < long_ma:
        return "SELL"
    else:
        return "HOLD"


# ==========================================
# MAIN PROGRAM
# ==========================================
if __name__ == "__main__":
    try:
        # Get last 200 daily bars using SIP feed
        bars = api.get_bars(
            "AAPL",
            tradeapi.TimeFrame.Day,
            limit=200,
            feed="sip"
        ).df

        if bars.empty:
            raise RuntimeError("No data returned from Alpaca.")

        prices = bars["close"].tolist()
        dates = bars.index

        # Moving averages over time
        short_ma = [
            moving_average(prices[:i+1], 50) if i >= 49 else None
            for i in range(len(prices))
        ]

        long_ma = [
            moving_average(prices[:i+1], 200) if i >= 199 else None
            for i in range(len(prices))
        ]

        signal = trade_decision(prices)
        current_price = prices[-1]

        print("AAPL Signal:", signal)
        print("Current Price:", current_price)

        # ==========================================
        # PLOT
        # ==========================================
        plt.figure(figsize=(12, 6))
        plt.plot(dates, prices, label="AAPL Price")
        plt.plot(dates, short_ma, label="50-Day MA")
        plt.plot(dates, long_ma, label="200-Day MA")

        plt.title(f"AAPL Live Chart — Signal: {signal}")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("ERROR:", e)
