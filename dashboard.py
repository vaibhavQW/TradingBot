# dashboard.py

from flask import Flask, render_template, jsonify
from database import fetch_all_trades, fetch_logs
from logger import log_message
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("dashboard.html")  # You'll need to create this HTML template


@app.route("/trades")
def trades():
    conn = sqlite3.connect("trading.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades ORDER BY timestamp DESC")
    trades = cursor.fetchall()
    conn.close()
    # Transform data into a list of dictionaries
    trade_list = []
    for trade in trades:
        trade_list.append(
            {
                "id": trade[0],
                "symbol": trade[1],
                "quantity": trade[2],
                "entry_price": trade[3],
                "target_price": trade[4],
                "stop_loss": trade[5],
                "order_id": trade[6],
                "timestamp": trade[7],
            }
        )
    return jsonify(trade_list)


@app.route("/logs")
def logs():
    conn = sqlite3.connect("trading.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 100")
    logs = cursor.fetchall()
    conn.close()
    log_list = []
    for log in logs:
        log_list.append(
            {"id": log[0], "level": log[1], "message": log[2], "timestamp": log[3]}
        )
    return jsonify(log_list)


if __name__ == "__main__":
    log_message("INFO", "Starting dashboard server.")
    app.run(host="0.0.0.0", port=5000)
