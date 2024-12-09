# reporting.py

import pandas as pd
import sqlite3
from config import DATABASE_PATH
from logger import log_message


def generate_monthly_report(month, year):
    """
    Generate a monthly trading report.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM trades
            WHERE strftime('%m', timestamp) = ?
            AND strftime('%Y', timestamp) = ?
        """,
            (f"{month:02d}", str(year)),
        )
        trades = cursor.fetchall()
        conn.close()

        if not trades:
            log_message(
                "INFO", f"No trades found for {month}/{year}. Report not generated."
            )
            return

        df = pd.DataFrame(
            trades,
            columns=[
                "id",
                "symbol",
                "quantity",
                "entry_price",
                "target_price",
                "stop_loss",
                "order_id",
                "timestamp",
            ],
        )
        df["profit_loss"] = (df["target_price"] - df["entry_price"]) * df["quantity"]
        total_pnl = df["profit_loss"].sum()
        win_trades = df[df["profit_loss"] > 0]
        loss_trades = df[df["profit_loss"] <= 0]

        report = {
            "Total Trades": len(df),
            "Winning Trades": len(win_trades),
            "Losing Trades": len(loss_trades),
            "Total PnL": round(total_pnl, 2),
            "Average PnL per Trade": round(df["profit_loss"].mean(), 2),
            "Win Rate": f"{(len(win_trades)/len(df))*100:.2f}%",
        }

        # Save report as CSV
        report_df = pd.DataFrame([report])
        report_df.to_csv(f"monthly_report_{month}_{year}.csv", index=False)
        log_message("INFO", f"Monthly report generated for {month}/{year}.")
    except Exception as e:
        log_message("ERROR", f"Error generating monthly report for {month}/{year}: {e}")
