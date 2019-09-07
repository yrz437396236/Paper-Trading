# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:47:17 2019

@author: 43739
"""

from backtesting_data_v12 import downloading
from backtesting_backtest_v12 import backtest
from backtesting_statistic_v12 import statistic

def core(auth_token,tickers,intra_freq,year):
    downloading(tickers,auth_token,intra_freq,year)
    params_dict=statistic(tickers,intra_freq,year)
    backtest(tickers,intra_freq,year,params_dict)    

if __name__ == '__main__':
    auth_token = 'b2407b4b35df301601ad4fbb8c849f10c2ba1f21'
    tickers = ['bp','rds-a'] 
    intra_freq = '1min'
    year='2018'
    core(auth_token,tickers,intra_freq,year)
