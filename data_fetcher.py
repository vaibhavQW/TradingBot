# data_fetcher.py

import yfinance as yf
from indicators import compute_rsi, compute_support_resistance
from config import NIFTY_STOCKS
from logger import log_message


def get_stock_data(symbol):
    """
    Fetch historical data for a given stock symbol.
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")  # Fetch last 1 month of data

        if hist.empty:
            log_message("WARNING", f"No data fetched for {symbol}.")
            return None

        # Calculate RSI and Support/Resistance
        hist = compute_rsi(hist)
        hist = compute_support_resistance(hist)

        # Get latest data point
        latest = hist.iloc[-1]
        return {
            "symbol": symbol,
            "close": round(latest["Close"], 2),
            "support": round(latest["Support"], 2),
            "resistance": round(latest["Resistance"], 2),
            "rsi": round(latest["RSI"], 2),
        }
    except Exception as e:
        log_message("ERROR", f"Error fetching data for {symbol}: {e}")
        return None


def fetch_all_stock_data():
    """
    Fetch data for all NIFTY stocks.
    """
    try:
        stock_data_list = []
        for symbol in NIFTY_STOCKS:
            data = get_stock_data(symbol)
            if data:
                stock_data_list.append(data)
        return stock_data_list
    except Exception as e:
        log_message("ERROR", f"Error fetching data for {symbol}: {e}")
        return None
