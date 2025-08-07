import json
import pandas as pd

BASE_URL = "https://api.coingecko.com/api/v3"

import requests

def get_price(coin_id: str = "bitcoin") -> float:
    """
    Fetch the current price of a cryptocurrency using the CoinGecko API.

    Args:
        coin_id (str): The CoinGecko ID of the coin (e.g., "bitcoin", "ethereum", "solana").
                       Defaults to "bitcoin".

    Returns:
        float: The current price of the coin in USD.

    Raises:
        requests.exceptions.RequestException: If the request fails.
        KeyError: If the expected data is not found in the response.
    """
    url = f"{BASE_URL}/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()[coin_id]["usd"]

def get_candlestick_data(coin_id: str = "bitcoin", days: int = 30) -> pd.DataFrame:
    """
    Fetch historical price data (used for candlestick charts) from CoinGecko.

    Args:
        coin_id (str): The CoinGecko ID of the coin (e.g., "bitcoin", "ethereum", "solana").
                       Defaults to "bitcoin".
        days (int): Number of days of historical data to retrieve (e.g., 1, 7, 30, 90, 365, "max").
                    Defaults to 30.

    Returns:
        pandas.DataFrame: A DataFrame containing:
            - timestamp (datetime): Time of the price point.
            - price (float): Price of the coin in USD at that time.

    Raises:
        requests.exceptions.RequestException: If the request fails.
        ValueError: If the API response cannot be parsed.
    """
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    prices = data.get("prices", [])

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def get_fundamentals(coin_id: str = "bitcoin") -> str:
    """
    Fetch fundamental data for a given cryptocurrency using its CoinGecko ID.

    Args:
        coin_id (str): The CoinGecko ID of the cryptocurrency (e.g., "bitcoin", "ethereum").
                       Defaults to "bitcoin".

    Returns:
        json: A dictionary containing the following fundamental data:
            - name (str): Full name of the cryptocurrency.
            - symbol (str): Uppercase ticker symbol (e.g., "BTC").
            - market_cap (float): Market capitalization in USD.
            - circulating_supply (float): Currently circulating supply.
            - total_supply (float or None): Total supply (may be None if not available).
            - rank (int): Market cap rank of the cryptocurrency.
            - description (str): First 250 characters of the English description.

    Raises:
        requests.exceptions.RequestException: If the network request fails.
        KeyError: If expected data fields are missing in the response.
    """
    url = f"{BASE_URL}/coins/{coin_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    result = {
        "name": data["name"],
        "symbol": data["symbol"].upper(),
        "market_cap": data["market_data"]["market_cap"]["usd"],
        "circulating_supply": data["market_data"]["circulating_supply"],
        "total_supply": data["market_data"]["total_supply"],
        "rank": data["market_cap_rank"],
        "description": data["description"]["en"][:500] + "..."
    }
    return json.dumps(result, indent=2)


def get_coins_market_data():
    """
    Fetch market data for top coins (market cap, symbol, id)
    """
    url = f"{BASE_URL}/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 250, "page": 1}
    data = requests.get(url, params=params).json()

    # Return mapping {symbol: {id, market_cap, name}}
    return {
        coin["symbol"].upper(): {
            "id": coin["id"],
            "name": coin["name"],
            "market_cap": coin["market_cap"]
        }
        for coin in data
    }