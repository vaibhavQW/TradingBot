# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Key
LLM_API_KEY = os.getenv("LLM_API_KEY")

# Brokerage API Credentials (Example: Zerodha Kite Connect)
BROKERAGE_API_KEY = os.getenv("BROKERAGE_API_KEY")
BROKERAGE_ACCESS_TOKEN = os.getenv("BROKERAGE_ACCESS_TOKEN")

# Data API Key (e.g., Alpha Vantage, Yahoo Finance)
DATA_API_KEY = os.getenv("DATA_API_KEY")

# Trading Parameters
CAPITAL = 5000  # Initial capital in INR
TARGET_PERCENT = 0.025  # 2.5% target per trade
STOP_LOSS_PERCENT = 0.015  # 1.5% stop-loss per trade

# List of NIFTY 50 Stocks (Example subset)
NIFTY_STOCKS = ["RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "HINDUNILVR.NS"]

# Database Configuration
DATABASE_PATH = "trading.db"

# Logging Configuration
LOG_FILE = "trading.log"

# Scheduler Configuration
TRADING_TIME = "10:00"  # 10 AM every weekday
TRADE_MANAGER_INTERVAL = "30"  # Minutes between trade manager runs

# Security Configuration
ENV_FILE = ".env"  # Ensure this file is added to .gitignore
