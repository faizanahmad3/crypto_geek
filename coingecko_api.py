import requests

BASE_URL = "https://api.coingecko.com/api/v3"

def get_fundamentals(coin_id="bitcoin"):
    url = f"{BASE_URL}/coins/{coin_id}"
    data = requests.get(url).json()
    return {
        "name": data["name"],
        "symbol": data["symbol"].upper(),
        "market_cap": data["market_data"]["market_cap"]["usd"],
        "circulating_supply": data["market_data"]["circulating_supply"],
        "total_supply": data["market_data"]["total_supply"],
        "rank": data["market_cap_rank"],
        "description": data["description"]["en"][:250] + "..."
    }

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