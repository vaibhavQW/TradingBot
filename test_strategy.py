# test_strategy.py

import unittest
from strategy import build_prompt, parse_llm_response
from data_fetcher import compute_rsi, compute_support_resistance
import pandas as pd


class TestStrategy(unittest.TestCase):
    def test_build_prompt(self):
        stock_data_list = [
            {
                "symbol": "RELIANCE.NS",
                "close": 200,
                "support": 195,
                "resistance": 206,
                "rsi": 42,
            },
            {
                "symbol": "HDFCBANK.NS",
                "close": 150,
                "support": 145,
                "resistance": 155,
                "rsi": 58,
            },
        ]
        prompt = build_prompt(stock_data_list)
        self.assertIn("RELIANCE.NS", prompt)
        self.assertIn("HDFCBANK.NS", prompt)
        self.assertIn("RSI 42", prompt)
        self.assertIn("RSI 58", prompt)

    def test_parse_llm_response_valid(self):
        response_text = "Buy RELIANCE.NS at 201, target 206, SL 198"
        trade_info = parse_llm_response(response_text)
        expected = {
            "symbol": "RELIANCE.NS",
            "entry_price": 201.0,
            "target_price": 206.0,
            "stop_loss": 198.0,
        }
        self.assertEqual(trade_info, expected)

    def test_parse_llm_response_invalid(self):
        response_text = "No suitable trade found today."
        trade_info = parse_llm_response(response_text)
        self.assertIsNone(trade_info)

    def test_compute_rsi(self):
        data = {
            "Close": [
                100,
                102,
                101,
                105,
                107,
                106,
                108,
                110,
                109,
                111,
                113,
                112,
                114,
                115,
                117,
            ]
        }
        df = pd.DataFrame(data)
        df = compute_rsi(df)
        self.assertIn("RSI", df.columns)
        self.assertFalse(df["RSI"].isnull().all())

    def test_compute_support_resistance(self):
        data = {
            "Close": [
                100,
                102,
                101,
                105,
                107,
                106,
                108,
                110,
                109,
                111,
                113,
                112,
                114,
                115,
                117,
            ]
        }
        df = pd.DataFrame(data)
        df = compute_support_resistance(df)
        self.assertIn("Support", df.columns)
        self.assertIn("Resistance", df.columns)
        self.assertFalse(df["Support"].isnull().all())
        self.assertFalse(df["Resistance"].isnull().all())


if __name__ == "__main__":
    unittest.main()
