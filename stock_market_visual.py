import os
import time
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

SYMBOL = "AAPL"
ORDER_SIZE = 10  # increase since you have 1M
last_signal = None


def moving_average(prices, days):
    return sum(prices[-days:]) / days


def trade_decision(prices):
    if len(prices) < 200:
        return "HOLD"

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


print("Bot running... Press CTRL+C to stop.")

while True:
    try:
        bars = api.get_bars(
            SYMBOL,
            tradeapi.TimeFrame.Day,
            limit=200,
            feed="sip"
        ).df

        prices = bars["close"].tolist()
        signal = trade_decision(prices)

        print("Signal:", signal)

        if signal != last_signal:

            if signal == "BUY":
                api.submit_order(
                    symbol=SYMBOL,
                    qty=ORDER_SIZE,
                    side="buy",
                    type="market",
                    time_in_force="gtc"
                )
                print("BUY order placed")

            elif signal == "SELL":
                api.submit_order(
                    symbol=SYMBOL,
                    qty=ORDER_SIZE,
                    side="sell",
                    type="market",
                    time_in_force="gtc"
                )
                print("SELL order placed")

            last_signal = signal

        time.sleep(60)  # wait 60 seconds

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
