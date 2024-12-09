# database.py

import sqlite3
from config import DATABASE_PATH
from logger import log_message


def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create trades table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            quantity INTEGER,
            entry_price REAL,
            target_price REAL,
            stop_loss REAL,
            order_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Create logs table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()
    log_message("INFO", "Database initialized.")


def insert_trade(trade_info):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO trades (symbol, quantity, entry_price, target_price, stop_loss, order_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            trade_info["symbol"],
            trade_info["quantity"],
            trade_info["entry_price"],
            trade_info["target_price"],
            trade_info["stop_loss"],
            trade_info["order_id"],
        ),
    )
    conn.commit()
    conn.close()
    log_message("INFO", f"Trade inserted into database: {trade_info}")


def fetch_all_trades():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades")
    trades = cursor.fetchall()
    conn.close()
    return trades


def log_message_to_db(level, message):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO logs (level, message)
        VALUES (?, ?)
    """,
        (level, message),
    )
    conn.commit()
    conn.close()
