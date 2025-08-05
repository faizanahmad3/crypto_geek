import pandas as pd

def calculate_rsi(df, period=14):
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def simple_moving_average(df, period=20):
    return df["close"].rolling(window=period).mean()

def detect_support_resistance(df):
    # Simple method: use local minima/maxima
    highs = df["high"].rolling(window=5).max()
    lows = df["low"].rolling(window=5).min()
    return {
        "resistance": round(highs.max(), 2),
        "support": round(lows.min(), 2)
    }
