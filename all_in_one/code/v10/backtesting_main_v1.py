# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:47:17 2019

@author: 43739
"""
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from backtesting_data_v1 import downloading
from backtesting_backtest_v1 import backtest

def statistics(tickers,intra_freq,year):
    stock1=pd.read_csv('data\\intra_'+tickers[0]+'_'+year+'_'+intra_freq+'.csv',index_col=0)
    stock2=pd.read_csv('data\\intra_'+tickers[1]+'_'+year+'_'+intra_freq+'.csv',index_col=0)
    close1=stock1['close'].values.reshape(-1, 1)
    close2=stock2['close'].values.reshape(-1, 1)
    reg=LinearRegression().fit(close2, close1)
    slope=reg.coef_[0][0]
    intercept=reg.intercept_[0] 
    res=stock2['close'].values*slope+intercept-stock1['close'].values
    std=np.std(res)
    params={'m':slope,'b':intercept,'std':std,'avg':0.5,'muti':1,'size':1000}
    return params

def core(auth_token,tickers,intra_freq,year):
    downloading(tickers,auth_token,intra_freq,year)
    params_dict=statistics(tickers,intra_freq,year)
    backtest(tickers,intra_freq,year,params_dict)
    

if __name__ == '__main__':
    auth_token = 'b2407b4b35df301601ad4fbb8c849f10c2ba1f21'
    tickers = ['bp','rds-a'] 
    intra_freq = '1min'
    year='2018'
    core(auth_token,tickers,intra_freq,year)
