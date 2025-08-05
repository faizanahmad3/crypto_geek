import requests
import pandas as pd

BASE_URL = "https://api.binance.com/api/v3"

def get_price(symbol="BTCUSDT"):
    url = f"{BASE_URL}/ticker/price"
    params = {"symbol": symbol.upper()}
    return float(requests.get(url, params=params).json()["price"])

def get_ohlc(symbol="BTCUSDT", interval="1h", limit=50):
    url = f"{BASE_URL}/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data, columns=[
        "timestamp","open","high","low","close","volume","close_time",
        "quote_asset_volume","num_trades","taker_buy_base","taker_buy_quote","ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df

def get_binance_symbols():
    url = f"{BASE_URL}/exchangeInfo"
    data = requests.get(url).json()
    symbols = [s["symbol"] for s in data["symbols"] if s["quoteAsset"] == "USDT"]
    base_coins = [s["baseAsset"] for s in data["symbols"] if s["quoteAsset"] == "USDT"]
    return list(set(base_coins))  # Unique coins


print(get_ohlc())