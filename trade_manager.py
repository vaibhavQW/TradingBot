# trade_manager.py

from broker_api import kite, get_open_positions
from database import fetch_all_trades, insert_trade
from logger import log_trade, log_message
from risk_management import adjust_trailing_stop
from config import TARGET_PERCENT, STOP_LOSS_PERCENT


def get_current_price(symbol):
    """
    Get the latest price for a given symbol.
    """
    try:
        ltp = kite.ltp(f"NSE:{symbol}")
        return ltp[f"NSE:{symbol}"]["last_price"]
    except Exception as e:
        log_message("ERROR", f"Error fetching current price for {symbol}: {e}")
        return None


def manage_trades():
    """
    Monitor and manage all open trades.
    """
    try:
        open_trades = get_open_positions()
        if not open_trades:
            log_message("INFO", "No open trades to manage.")
            return

        for trade in open_trades:
            symbol = trade["tradingsymbol"]
            quantity = trade["quantity"]
            entry_price = trade["average_price"]
            target_price = entry_price * (1 + TARGET_PERCENT)
            stop_loss = entry_price * (1 - STOP_LOSS_PERCENT)

            current_price = get_current_price(symbol)
            if current_price is None:
                continue  # Skip if unable to fetch price

            # Check if target or stop-loss is hit
            if current_price >= target_price:
                # Sell at target
                sell_order_id = kite.place_order(
                    variety=kite.VARIETY_REGULAR,
                    exchange=kite.EXCHANGE_NSE,
                    tradingsymbol=symbol,
                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                    quantity=quantity,
                    product=kite.PRODUCT_MIS,
                    order_type=kite.ORDER_TYPE_LIMIT,
                    price=target_price,
                    validity=kite.VALIDITY_DAY,
                    disclosed_quantity=0,
                    trigger_price=None,
                    squareoff=None,
                    stoploss=None,
                    trailing_stoploss=None,
                )
                trade_record = {
                    "symbol": symbol,
                    "quantity": quantity,
                    "entry_price": entry_price,
                    "target_price": target_price,
                    "stop_loss": stop_loss,
                    "order_id": sell_order_id,
                }
                log_trade(
                    {
                        "symbol": symbol,
                        "action": "SELL",
                        "price": target_price,
                        "reason": "Target reached",
                        "order_id": sell_order_id,
                    }
                )
                log_message("INFO", f"Sold {symbol} at target price ₹{target_price}")

            elif current_price <= stop_loss:
                # Sell at stop-loss
                sell_order_id = kite.place_order(
                    variety=kite.VARIETY_REGULAR,
                    exchange=kite.EXCHANGE_NSE,
                    tradingsymbol=symbol,
                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                    quantity=quantity,
                    product=kite.PRODUCT_MIS,
                    order_type=kite.ORDER_TYPE_LIMIT,
                    price=stop_loss,
                    validity=kite.VALIDITY_DAY,
                    disclosed_quantity=0,
                    trigger_price=None,
                    squareoff=None,
                    stoploss=None,
                    trailing_stoploss=None,
                )
                trade_record = {
                    "symbol": symbol,
                    "quantity": quantity,
                    "entry_price": entry_price,
                    "target_price": target_price,
                    "stop_loss": stop_loss,
                    "order_id": sell_order_id,
                }
                log_trade(
                    {
                        "symbol": symbol,
                        "action": "SELL",
                        "price": stop_loss,
                        "reason": "Stop-loss triggered",
                        "order_id": sell_order_id,
                    }
                )
                log_message("INFO", f"Sold {symbol} at stop-loss price ₹{stop_loss}")

            else:
                # Optional: Implement trailing stop-loss
                new_stop_loss = adjust_trailing_stop(current_price)
                if new_stop_loss > stop_loss:
                    try:
                        kite.modify_order(
                            variety=kite.VARIETY_REGULAR,
                            order_id=trade["order_id"],
                            price=trade["entry_price"],  # Maintain entry price
                            trigger_price=new_stop_loss,
                            validity=kite.VALIDITY_DAY,
                        )
                        log_message(
                            "INFO",
                            f"Trailing stop-loss updated for {symbol} to ₹{new_stop_loss}",
                        )
                    except Exception as e:
                        log_message(
                            "ERROR",
                            f"Error updating trailing stop-loss for {symbol}: {e}",
                        )
    except Exception as e:
        log_message("ERROR", f"Unexpected error in trade manager: {e}")


if __name__ == "__main__":
    manage_trades()
