# diversification.py

from config import NIFTY_STOCKS
from logger import log_message


def diversify_portfolio(selected_trades):
    """
    Ensure diversification by limiting the number of trades per sector.
    """
    sector_limits = {
        "Banking": 2,
        "IT": 2,
        "Energy": 1,
        "Consumer": 2,
        # Add more sectors and limits as needed
    }

    sector_counts = {sector: 0 for sector in sector_limits}
    diversified_trades = []

    for trade in selected_trades:
        sector = get_sector(trade["symbol"])
        if sector and sector_counts.get(sector, 0) < sector_limits.get(sector, 0):
            diversified_trades.append(trade)
            sector_counts[sector] += 1
        else:
            log_message(
                "WARNING",
                f"Trade for {trade['symbol']} excluded to maintain diversification.",
            )

    return diversified_trades


def get_sector(symbol):
    """
    Retrieve the sector of a given stock symbol.
    """
    sector_mapping = {
        "RELIANCE.NS": "Energy",
        "HDFCBANK.NS": "Banking",
        "TCS.NS": "IT",
        "INFY.NS": "IT",
        "HINDUNILVR.NS": "Consumer",
        # Add more mappings as needed
    }
    return sector_mapping.get(symbol, None)
