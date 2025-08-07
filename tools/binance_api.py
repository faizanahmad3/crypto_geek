import requests
import pandas as pd
from pandas import DataFrame
from datetime import datetime

BASE_URL = "https://api.binance.com/api/v3"

def get_price(symbol: str = "BTCUSDT") -> float:
    """
    Fetch the latest price of a given cryptocurrency trading pair from Binance.

    Args:
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
                      Defaults to "BTCUSDT".

    Returns:
        float: The latest price of the trading pair.

    Raises:
        requests.exceptions.RequestException: If there is a network-related error.
        KeyError: If the response does not contain the "price" field.
        ValueError: If the price value cannot be converted to float.
    """
    url = f"{BASE_URL}/ticker/price"
    params = {"symbol": symbol.upper()}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return float(response.json()["price"])


def get_candlestick_data(symbol: str = "BTCUSDT", interval: str = "1d", limit: int = 365) -> DataFrame:
    """
    Fetch OHLC (Open-High-Low-Close) candlestick data for a given trading pair.

    Args:
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
                      Defaults to "BTCUSDT".
        interval (str): Candlestick interval (e.g., "1m", "5m", "1h", "1d").
                        Defaults to "1d".
        limit (int): Number of data points to retrieve (maximum 1000).
                     Defaults to 365.

    Returns:
        pandas.DataFrame: A DataFrame containing candlestick data with columns:
            - timestamp
            - open
            - high
            - low
            - close
            - volume
            - close_time
            - quote_asset_volume
            - num_trades
            - taker_buy_base
            - taker_buy_quote
            - ignore

        The 'close' column is cast to float for numerical analysis.

    Raises:
        requests.exceptions.RequestException: If there is a network-related error.
        ValueError: If the API response cannot be parsed.
    """
    url = f"{BASE_URL}/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "num_trades", "taker_buy_base", "taker_buy_quote", "ignore"
    ])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')

    df["close"] = df["close"].astype(float)
    return df

def get_binance_symbols():
    url = f"{BASE_URL}/exchangeInfo"
    data = requests.get(url).json()
    symbols = [s["symbol"] for s in data["symbols"] if s["quoteAsset"] == "USDT"]
    base_coins = [s["baseAsset"] for s in data["symbols"] if s["quoteAsset"] == "USDT"]
    return list(set(base_coins))  # Unique coins


# print(get_candlestick_data(symbol="GALAUSDT", interval="1d", limit=365))
