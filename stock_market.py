# stock_market.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# ===============================
# Binary Tree Node
# ===============================
class TreeNode:
    def __init__(self, value, label):
        self.value = value      # numeric value
        self.label = label      # P, SMA, LMA
        self.left = None
        self.right = None


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
# Build Binary Tree (Least → Greatest)
# ===============================
def build_tree(price, shortMA, longMA):
    root = TreeNode(price, "P")

    if shortMA < price:
        root.left = TreeNode(shortMA, "SMA")
        root.right = TreeNode(longMA, "LMA")
    else:
        root.left = TreeNode(longMA, "LMA")
        root.right = TreeNode(shortMA, "SMA")

    return root


# ===============================
# API
# ===============================
app = FastAPI(title="Stock Market API")

class PriceData(BaseModel):
    prices: List[float]

@app.post("/trade/aapl")
def trade_aapl(data: PriceData):
    signal = trade_decision(data.prices)
    return {
        "stock": "AAPL",
        "signal": signal
    }


# ===============================
# Local Test (Runs without API)
# ===============================
if __name__ == "__main__":
    # Test data designed to trigger BUY
    prices = [150] * 200 + [160, 165, 170, 175, 180, 185, 190, 195, 200, 205]

    price = prices[-1]
    shortMA = moving_average(prices, 50)
    longMA = moving_average(prices, 200)

    tree = build_tree(price, shortMA, longMA)
    signal = trade_decision(prices)

    print("AAPL Signal:", signal)
    print("Binary Tree:")
    print(f" Root → {tree.label}:{tree.value}")
    print(f" Left → {tree.left.label}:{tree.left.value}")
    print(f" Right → {tree.right.label}:{tree.right.value}")
