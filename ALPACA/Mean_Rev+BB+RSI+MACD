import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import ccxt
import alpaca_trade_api as tradeapi
import backtrader as bt
import backtrader.feeds as btfeeds
from backtrader import Strategy


class MeanReversionStrategy(Strategy):
    """
    Mean Reversion Strategy using Bollinger Bands, RSI, and MACD.
    """
    params = (('bb_period', 20), ('rsi_period', 14), ('macd_fast', 12), ('macd_slow', 26), ('macd_signal', 9))

    def init(self):
        self.bb = ta.bbands(self.params.bb_period)
        self.rsi = ta.rsi(self.params.rsi_period)
        self.macd = ta.macd(self.params.macd_fast,self.params.macd_slow, self.params.macd_signal)

    def next(self):
        if self.bb.lines['bot'] < self.data.close and self.rsi < 30 and self.macd > 0:
            self.buy()
        elif self.bb.lines['top'] > self.data.close and self.rsi > 70 and self.macd < 0:
            self.sell()


# Create a cerebro entity
cerebro = bt.Cerebro()

# Create a data feed
data = yf.download(tickers='BTC-USD', start='2023-01-01', end='2023-12-31')

# Create data feed
data_feed = bt.feeds.PandasData(dataname=data)

# Add data feed
cerebro.adddata(data_feed)

# Add strategy
cerebro.addstrategy(MeanReversionStrategy)

# Set initial cash
cerebro.broker.setcash(10000.0)

# Add sizer
cerebro.addsizer(bt.sizers.FixedSize, stake=10)

# Run the strategy
cerebro.run()

# Plot the results
cerebro.plot()

# Get the performance statistics
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Annual Return: %.2f%%' % ((cerebro.broker.getvalue() / 10000.0) - 1) * 100)

# Evaluate the strategy performance
print('Strategy Evaluation:')
print('-------------------')
print('Total Trades: ', cerebro.stats.broker.total.trades)
print('Winning Trades: ', cerebro.stats.broker.won.trades)
print('Losing Trades: ', cerebro.stats.broker.lost.trades)
print('Win/Loss Ratio: ', cerebro.stats.broker.won.trades / cerebro.stats.broker.lost.trades)
print('Average Win: ', cerebro.stats.broker.won.pnl.mean())
print('Average Loss: ', cerebro.stats.broker.lost.pnl.mean())
print('Profit Factor: ', cerebro.stats.broker.won.pnl.sum() / cerebro.stats.broker.lost.pnl.sum())
