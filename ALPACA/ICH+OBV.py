import pandas as pd
import yfinance as yf
import numpy as np
import backtrader as bt
from backtrader import Strategy
import ccxt

class ICH_OBV(Strategy):
    symbols = ['BTC/USD', 'ETH/USD', 'LTC/USD', 'XRP/USD', 'BCH/USD']
    def __init__(self):
        TIMEFRAME = '5m'
        FETCHING_LIMIT = 105120  # 1 year (525600 minutes / 5 minute timeframe)
        TRADE_SIZE = 0.0004  
        STOP_LOSS = 0.05  
        MAX_LOSSES = 3
        
    def strategy_ic_obv(data, conversion_line, base_line, span_a, span_b, obv_window):
        data['conversion_line'] = (data['High'] + data['Low']) / 2
        data['base_line'] = (data['High'] + data['Low'] + data['Close']) / 3
        data['span_a'] = ((data['High'] + data['Low']) / 2).shift(conversion_line)
        data['span_b'] = ((data['High'] + data['Low']) / 2).shift(base_line)
    
        data['obv'] = data['Volume'] * np.sign(data['Close'].diff(1))
        data['obv_ma'] = data['obv'].rolling(window=obv_window).mean()
    
        data['signal'] = np.where((data['Close'] > data['span_a']) & (data['obv_ma'] > 0), 1, 
                              np.where((data['Close'] < data['span_b']) & (data['obv_ma'] < 0), -1, 0))
    
        return data

data = yf.download(tickers=ICH_OBV.symbols, start='2017-01-01', end='2022-02-26')
cerebro = bt.Cerebro()

cerebro.adddata(data)
cerebro.addstrategy(ICH_OBV)
cerebro.broker.setcash(1000.0)
cerebro.run()
