# broker_api.py

from kiteconnect import KiteConnect
from config import BROKERAGE_API_KEY, BROKERAGE_ACCESS_TOKEN
from logger import log_message

# Initialize Kite Connect
kite = KiteConnect(api_key=BROKERAGE_API_KEY)
kite.set_access_token(BROKERAGE_ACCESS_TOKEN)


def place_order(symbol, quantity, price, transaction_type="BUY"):
    """
    Place an order with the brokerage.
    """
    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=transaction_type,
            quantity=quantity,
            product=kite.PRODUCT_MIS,  # Intraday product
            order_type=kite.ORDER_TYPE_LIMIT,
            price=price,
            validity=kite.VALIDITY_DAY,
            disclosed_quantity=0,
            trigger_price=None,
            squareoff=None,
            stoploss=None,
            trailing_stoploss=None,
        )
        log_message("INFO", f"Order placed successfully. Order ID: {order_id}")
        return order_id
    except Exception as e:
        log_message("ERROR", f"Error placing order for {symbol}: {e}")
        return None


def get_open_positions():
    """
    Retrieve all open positions.
    """
    try:
        positions = kite.positions()
        return positions["day"]  # Intraday positions
    except Exception as e:
        log_message("ERROR", f"Error fetching open positions: {e}")
        return []
