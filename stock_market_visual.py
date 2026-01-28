# stock_market_visual.py

import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt

# ===============================
# Alpaca API credentials
# ===============================
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_SECRET_KEY"
BASE_URL = "https://paper-api.alpaca.markets"  # Paper trading

# Connect to Alpaca
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# ===============================
# Moving Average
# ===============================
def moving_average(prices, days):
    return sum(prices[-days:]) / days

# ===============================
# Trading Algorithm
# ===============================
def trade_decision(prices):
    if len(prices) < 200:
        return "NOT ENOUGH DATA"

    shortMA = moving_average(prices, 50)
    longMA = moving_average(prices, 200)

    prevShortMA = moving_average(prices[:-1], 50)
    prevLongMA = moving_average(prices[:-1], 200)

    if prevShortMA <= prevLongMA and shortMA > longMA:
        return "BUY"
    elif prevShortMA >= prevLongMA and shortMA < longMA:
        return "SELL"
    else:
        return "HOLD"

# ===============================
# Main Program
# ===============================
if __name__ == "__main__":
    # Get last 200 daily bars for AAPL
    barset = api.get_bars("AAPL", tradeapi.TimeFrame.Day, limit=200).df
    prices = barset['close'].tolist()
    dates = barset.index.tolist()

    # Moving averages
    short_ma_list = [moving_average(prices[:i+1], 50) if i >= 49 else None for i in range(len(prices))]
    long_ma_list = [moving_average(prices[:i+1], 200) if i >= 199 else None for i in range(len(prices))]

    # Current signal
    signal = trade_decision(prices)

    # Print info
    print(f"AAPL Trading Signal: {signal}")

    # ===============================
    # Plot the stock and MAs
    # ===============================
    plt.figure(figsize=(12,6))
    plt.plot(dates, prices, label="AAPL Price", color="blue")
    plt.plot(dates, short_ma_list, label="50-day MA", color="green")
    plt.plot(dates, long_ma_list, label="200-day MA", color="red")
    plt.title(f"AAPL Stock Price & Moving Averages — Signal: {signal}")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
