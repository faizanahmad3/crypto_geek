import streamlit as st
from binance_api import get_price, get_ohlc, get_binance_symbols
from coingecko_api import get_fundamentals, get_coins_market_data
from indicators import calculate_rsi, detect_support_resistance

# ------------------------------
# Streamlit Config
# ------------------------------
st.set_page_config(page_title="Crypto Data Agent", layout="wide")
st.title("Crypto Data Fetcher (For LLM)")

# ------------------------------
# Fetch Coin List (Dynamic)
# ------------------------------

# Get Binance USDT pairs
binance_coins = get_binance_symbols()

# Get CoinGecko market data
market_data = get_coins_market_data()

# Filter coins present on both Binance and CoinGecko
available_coins = {
    sym: info for sym, info in market_data.items() if sym in binance_coins
}

# Sort by market cap
sorted_coins = sorted(available_coins.items(), key=lambda x: x[1]["market_cap"], reverse=True)

# Dropdown display format: Bitcoin (BTC)
coin_names = [f"{v['name']} ({k})" for k, v in sorted_coins]

# ------------------------------
# User Select Coin
# ------------------------------
selected_coin_display = st.selectbox("Select a Coin", coin_names)

# Extract symbol & ID
selected_symbol = selected_coin_display.split("(")[-1].replace(")", "")
coin_id = available_coins[selected_symbol]["id"]

# ------------------------------
# Button to Fetch Data
# ------------------------------
if st.button("Get Coin Info"):

    # --- Fetch Real-Time Price ---
    price = get_price(f"{selected_symbol}USDT")

    # --- Fundamentals (CoinGecko) ---
    fundamentals = get_fundamentals(coin_id)

    # --- OHLC & Technicals ---
    ohlc_df = get_ohlc(f"{selected_symbol}USDT", interval="1h", limit=50)
    rsi = calculate_rsi(ohlc_df).iloc[-1]
    sr = detect_support_resistance(ohlc_df)

    # ------------------------------
    # Prepare Data Summary
    # ------------------------------
    info = {
        "name": fundamentals['name'],
        "symbol": selected_symbol,
        "price": price,
        "market_cap": fundamentals['market_cap'],
        "rank": fundamentals['rank'],
        "circulating_supply": fundamentals['circulating_supply'],
        "total_supply": fundamentals['total_supply'],
        "rsi": round(rsi, 2),
        "support": sr['support'],
        "resistance": sr['resistance'],
        "description": fundamentals['description']
    }

    # ------------------------------
    # Print to Terminal (for debugging / LLM use)
    # ------------------------------
    print("\n========== COIN DATA ==========")
    for key, value in info.items():
        print(f"{key}: {value}")
    print("================================\n")

    # ------------------------------
    # Show in Streamlit
    # ------------------------------
    st.subheader(f"{info['name']} ({info['symbol']})")
    st.write(f"**Price:** {info['price']}")
    st.write(f"**Market Cap:** ${info['market_cap']:,.0f}")
    st.write(f"**Rank:** #{info['rank']}")
    st.write(f"**Circulating Supply:** {info['circulating_supply']:,.0f}")
    st.write(f"**Total Supply:** {info['total_supply']:,.0f}")
    st.write(f"**RSI:** {info['rsi']} → "
             f"{'Overbought' if info['rsi'] > 70 else 'Oversold' if info['rsi'] < 30 else 'Neutral'}")
    st.write(f"**Support Level:** ${info['support']}")
    st.write(f"**Resistance Level:** ${info['resistance']}")
    st.write(f"**Description:** {info['description']}")

