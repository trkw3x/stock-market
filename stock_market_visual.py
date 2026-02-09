# stock_market_visual.py

import os
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt

# ===============================
# Alpaca API credentials
# ===============================
API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")

BASE_URL = "https://paper-api.alpaca.markets"

if not API_KEY or not API_SECRET:
    raise RuntimeError("Alpaca API keys not found in environment variables.")

api = tradeapi.REST(
    API_KEY,
    API_SECRET,
    BASE_URL,
    api_version="v2"
)

# ===============================
# Moving Average
# ===============================
def moving_average(prices, days):
    return sum(prices[-days:]) / days


# ===============================
# Trading Logic
# ===============================
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


# ===============================
# Main
# ===============================
if __name__ == "__main__":
    bars = api.get_bars("AAPL", tradeapi.TimeFrame.Day, limit=200).df

    prices = bars["close"].tolist()
    dates = bars.index

    short_ma = [moving_average(prices[:i+1], 50) if i >= 49 else None for i in range(len(prices))]
    long_ma = [moving_average(prices[:i+1], 200) if i >= 199 else None for i in range(len(prices))]

    signal = trade_decision(prices)
    print("AAPL Signal:", signal)

    plt.figure(figsize=(12,6))
    plt.plot(dates, prices, label="Price")
    plt.plot(dates, short_ma, label="50 MA")
    plt.plot(dates, long_ma, label="200 MA")
    plt.title(f"AAPL — {signal}")
    plt.legend()
    plt.grid()
    plt.show()
