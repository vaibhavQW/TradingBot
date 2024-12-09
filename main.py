# main.py

from data_fetcher import fetch_all_stock_data
from strategy import build_prompt, parse_llm_response
from llm_client import query_llm
from broker_api import place_order
from logger import log_trade, log_message
from database import insert_trade
from risk_management import calculate_dynamic_position_size
from ml_models import train_ml_model, predict_trade_success
from sentiment_analysis import get_news_sentiment
from diversification import diversify_portfolio
from reporting import generate_monthly_report
from config import CAPITAL, STOP_LOSS_PERCENT, NIFTY_STOCKS

# Initialize and train the ML model at startup
model = train_ml_model()


def integrate_sentiment(stock_data_list):
    """
    Enhance stock data with sentiment analysis.
    """
    enhanced_data = []
    for stock in stock_data_list:
        sentiment = get_news_sentiment(stock["symbol"])
        stock["sentiment"] = sentiment
        enhanced_data.append(stock)
    return enhanced_data


def filter_trades_with_ml_and_sentiment(trade_info, model):
    """
    Use ML predictions and sentiment to decide whether to execute the trade.
    """
    if not model:
        log_message(
            "WARNING", "ML model not available. Proceeding without ML filtering."
        )
        return True  # Proceed with the trade

    prediction = predict_trade_success(model, trade_info)
    sentiment = trade_info.get("sentiment", "Neutral")

    log_message(
        "INFO",
        f"ML Prediction for {trade_info['symbol']}: {'Success' if prediction else 'Failure'}",
    )
    log_message("INFO", f"Sentiment for {trade_info['symbol']}: {sentiment}")

    # Define criteria for accepting the trade
    if prediction and sentiment == "Positive":
        return True
    else:
        log_message(
            "WARNING", f"Trade for {trade_info['symbol']} filtered out by ML/sentiment."
        )
        return False


def apply_diversification(trades):
    """
    Ensure that the selected trades are diversified across different sectors.
    """
    diversified_trades = diversify_portfolio(trades)
    log_message(
        "INFO",
        f"Diversified Trades: {[trade['symbol'] for trade in diversified_trades]}",
    )
    return diversified_trades


def main():
    try:
        # Step 1: Fetch Market Data
        stock_data_list = fetch_all_stock_data()
        if not stock_data_list:
            log_message("WARNING", "No stock data fetched. Exiting trade execution.")
            return

        # Step 2: Enhance Data with Sentiment Analysis
        stock_data_list = integrate_sentiment(stock_data_list)

        # Step 3: Build Prompt and Query LLM
        prompt = build_prompt(stock_data_list)
        llm_response = query_llm(prompt)

        if llm_response:
            print("LLM Response:", llm_response)
            trade_info = parse_llm_response(llm_response)

            if trade_info:
                # Add sentiment to trade_info
                symbol = trade_info["symbol"]
                sentiment = next(
                    (
                        item["sentiment"]
                        for item in stock_data_list
                        if item["symbol"] == symbol
                    ),
                    "Neutral",
                )
                trade_info["sentiment"] = sentiment

                # Step 4: ML and Sentiment Filtering
                proceed = filter_trades_with_ml_and_sentiment(trade_info, model)

                if not proceed:
                    log_message(
                        "WARNING", f"Trade for {symbol} rejected based on ML/sentiment."
                    )
                    return

                # Step 5: Calculate Quantity based on Risk Management
                quantity = calculate_dynamic_position_size(
                    capital=CAPITAL,
                    risk_per_trade=STOP_LOSS_PERCENT,
                    entry_price=trade_info["entry_price"],
                    stop_loss_price=trade_info["stop_loss"],
                )

                if quantity <= 0:
                    log_message(
                        "WARNING",
                        "Calculated quantity is zero or negative. Skipping trade.",
                    )
                    return

                # Step 6: Place Order
                order_id = place_order(
                    symbol=trade_info["symbol"],
                    quantity=quantity,
                    price=trade_info["entry_price"],
                    transaction_type="BUY",
                )

                if order_id:
                    # Step 7: Log the Trade
                    trade_record = {
                        "symbol": trade_info["symbol"],
                        "quantity": quantity,
                        "entry_price": trade_info["entry_price"],
                        "target_price": trade_info["target_price"],
                        "stop_loss": trade_info["stop_loss"],
                        "order_id": order_id,
                    }
                    log_trade(trade_record)
                    insert_trade(trade_record)
        else:
            log_message("ERROR", "No response from LLM. No trade executed.")
    except Exception as e:
        log_message("ERROR", f"Unexpected error in main trading script: {e}")


if __name__ == "__main__":
    main()
