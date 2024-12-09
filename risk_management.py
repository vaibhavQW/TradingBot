# risk_management.py


def calculate_dynamic_position_size(
    capital, risk_per_trade, entry_price, stop_loss_price
):
    """
    Calculate the number of shares to buy based on capital, risk per trade, and stop-loss.
    """
    risk_amount = capital * risk_per_trade  # e.g., 1.5% of capital
    per_share_risk = entry_price - stop_loss_price
    if per_share_risk <= 0:
        return 0
    quantity = int(risk_amount / per_share_risk)
    return quantity


def adjust_trailing_stop(current_price, entry_price, trailing_stop_percent=0.005):
    """
    Calculate a new trailing stop based on the current price.
    """
    return current_price * (1 - trailing_stop_percent)
