# strategy.py

import re


def build_prompt(stock_data_list):
    """
    Construct a prompt for the LLM based on fetched stock data.
    """
    prompt = "You are my trading assistant. Our goal is to achieve 5–10% monthly returns on a ₹5000 capital.\n"
    prompt += "Here is the current data for today's trading candidates:\n"
    for stock in stock_data_list:
        prompt += (
            f"- {stock['symbol']}: Close ₹{stock['close']}, Support ₹{stock['support']}, "
            f"Resistance ₹{stock['resistance']}, RSI {stock['rsi']}\n"
        )
    prompt += "Suggest one stock to buy with entry price, target price (~2-3% above entry), and stop-loss (~1-2% below entry)."
    return prompt


def parse_llm_response(response_text):
    """
    Parse the LLM's response to extract trade details.
    Expected format: "Buy RELIANCE.NS at 201, target 206, SL 198"
    """
    symbol_match = re.search(r"Buy\s+([A-Z\.]+)", response_text, re.IGNORECASE)
    entry_match = re.search(r"at\s+(\d+\.?\d*)", response_text, re.IGNORECASE)
    target_match = re.search(r"target\s+(\d+\.?\d*)", response_text, re.IGNORECASE)
    sl_match = re.search(r"SL\s+(\d+\.?\d*)", response_text, re.IGNORECASE)

    if symbol_match and entry_match and target_match and sl_match:
        return {
            "symbol": symbol_match.group(1).upper(),
            "entry_price": float(entry_match.group(1)),
            "target_price": float(target_match.group(1)),
            "stop_loss": float(sl_match.group(1)),
        }
    else:
        print("Failed to parse LLM response.")
        return None
