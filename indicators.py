# indicators.py

import ta


def compute_rsi(df, window=14):
    """
    Compute Relative Strength Index (RSI) for the given dataframe.
    """
    try:
        rsi_indicator = ta.momentum.RSIIndicator(close=df["Close"], window=window)
        df["RSI"] = rsi_indicator.rsi()
    except Exception as e:
        print(f"Error computing RSI: {e}")
        df["RSI"] = 50  # Neutral value in case of error
    return df


def compute_support_resistance(df):
    """
    Compute simple support and resistance levels based on rolling window.
    """
    try:
        window = 20  # Number of days to consider
        df["Support"] = df["Close"].rolling(window=window).min()
        df["Resistance"] = df["Close"].rolling(window=window).max()
    except Exception as e:
        print(f"Error computing support/resistance: {e}")
        df["Support"] = df["Close"] - 10  # Arbitrary fallback
        df["Resistance"] = df["Close"] + 10
    return df
