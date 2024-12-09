# scheduler.py

import schedule
import time
import subprocess
from logger import log_message


def run_main():
    try:
        log_message("INFO", "Running main trading script.")
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        log_message("ERROR", f"Main trading script failed: {e}")


def run_trade_manager():
    try:
        log_message("INFO", "Running trade manager script.")
        subprocess.run(["python", "trade_manager.py"], check=True)
    except subprocess.CalledProcessError as e:
        log_message("ERROR", f"Trade manager script failed: {e}")


def setup_schedule():
    # Schedule the main trading script to run every weekday at TRADING_TIME
    schedule.every().monday.at("10:00").do(run_main)
    schedule.every().tuesday.at("10:00").do(run_main)
    schedule.every().wednesday.at("10:00").do(run_main)
    schedule.every().thursday.at("10:00").do(run_main)
    schedule.every().friday.at("10:00").do(run_main)

    # Schedule the trade manager to run every TRADE_MANAGER_INTERVAL minutes during market hours (9 AM to 3 PM)
    # Assuming market hours 9 AM to 3 PM
    def trade_manager_job():
        run_trade_manager()

    for hour in range(9, 16):
        for minute in [0, 30]:
            time_str = f"{hour:02d}:{minute:02d}"
            schedule.every().monday.at(time_str).do(trade_manager_job)
            schedule.every().tuesday.at(time_str).do(trade_manager_job)
            schedule.every().wednesday.at(time_str).do(trade_manager_job)
            schedule.every().thursday.at(time_str).do(trade_manager_job)
            schedule.every().friday.at(time_str).do(trade_manager_job)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    setup_schedule()
