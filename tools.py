from langchain.tools import tool
from binance_api import get_price, get_ohlc
from coingecko_api import get_fundamentals
from indicators import calculate_rsi, detect_support_resistance

@tool
def fetch_price(symbol: str) -> str:
    """Fetch real-time price of a coin from Binance (symbol like BTCUSDT)."""
    return str(get_price(symbol))

@tool
def fetch_fundamentals(coin_id: str) -> str:
    """Fetch fundamental data of a coin from CoinGecko (coin_id like 'bitcoin')."""
    data = get_fundamentals(coin_id)
    return str(data)

@tool
def fetch_technical(symbol: str) -> str:
    """Fetch OHLC data and return RSI + support/resistance for a symbol."""
    df = get_ohlc(symbol, interval="1h", limit=50)
    rsi = calculate_rsi(df).iloc[-1]
    sr = detect_support_resistance(df)
    return f"RSI: {round(rsi,2)}, Support: {sr['support']}, Resistance: {sr['resistance']}"
