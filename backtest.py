# backtest.py

import backtrader as bt
from datetime import datetime
from data_fetcher import get_stock_data
from indicators import compute_rsi, compute_support_resistance
from logger import log_message


class LLMStrategy(bt.Strategy):
    params = (
        ("rsi_period", 14),
        ("rsi_overbought", 70),
        ("rsi_oversold", 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.rsi_period)

    def next(self):
        if not self.position:
            if self.rsi < self.params.rsi_oversold:
                self.buy()
        elif self.rsi > self.params.rsi_overbought:
            self.sell()


def run_backtest(
    symbol="RELIANCE.NS", fromdate=datetime(2020, 1, 1), todate=datetime(2021, 1, 1)
):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(LLMStrategy)

    # Fetch historical data using yfinance
    data = bt.feeds.YahooFinanceData(dataname=symbol, fromdate=fromdate, todate=todate)
    cerebro.adddata(data)

    cerebro.broker.set_cash(5000)
    log_message("INFO", f"Starting Backtest for {symbol} from {fromdate} to {todate}.")
    cerebro.run()
    log_message(
        "INFO",
        f"Backtest completed for {symbol}. Final Portfolio Value: {cerebro.broker.getvalue()}",
    )
    cerebro.plot()


if __name__ == "__main__":
    run_backtest()
