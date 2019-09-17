# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 13:07:53 2019

@author: 43739
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
from backtesting_filter_v13 import delete_abrupt_time
from scipy.stats import kurtosis

def statistic(tickers,intra_freq,year):
    stock1=pd.read_csv('data\\intra_'+tickers[0]+'_'+year+'_'+intra_freq+'.csv',index_col=0)
    stock2=pd.read_csv('data\\intra_'+tickers[1]+'_'+year+'_'+intra_freq+'.csv',index_col=0)
    statistic_original(stock1,stock2,tickers)
    params=statistic_filtered(stock1,stock2,tickers,intra_freq,year)  
    return params

def statistic_filtered(stock1,stock2,tickers,intra_freq,year):
    stock1=delete_abrupt_time(stock1)
    stock2=delete_abrupt_time(stock2)
    stock1.to_csv('data\\intra_'+tickers[0]+'_'+year+'_'+intra_freq+'_filtered.csv')
    stock2.to_csv('data\\intra_'+tickers[1]+'_'+year+'_'+intra_freq+'_filtered.csv')
    close1=stock1['close'].values.reshape(-1, 1)
    close2=stock2['close'].values.reshape(-1, 1)
    reg=LinearRegression().fit(close2, close1)
    slope=reg.coef_[0][0]
    intercept=reg.intercept_[0] 
    res=stock2['close'].values*slope+intercept-stock1['close'].values
    kts=kurtosis(res)+3#compare to normal
    std=np.std(res)
    params={'m':slope,'b':intercept,'std':std,'avg':0.5,'muti':1,'size':1000,'kurtosis':kts}
    ########################################################################
    #statistic plots
    res_hist_kernel_normal(tickers,res,params,original=False)
    cor_plot(tickers,stock1,stock2,params,original=False)
    ########################################################################    
    return params

def statistic_original(stock1,stock2,tickers):
    close1=stock1['close'].values.reshape(-1, 1)
    close2=stock2['close'].values.reshape(-1, 1)
    reg=LinearRegression().fit(close2, close1)
    slope=reg.coef_[0][0]
    intercept=reg.intercept_[0] 
    res=stock2['close'].values*slope+intercept-stock1['close'].values
    kts=kurtosis(res)+3
    std=np.std(res)
    params={'m':slope,'b':intercept,'std':std,'avg':0.5,'muti':1,'size':1000,'kurtosis':kts}
    ########################################################################
    #statistic plots
    res_hist_kernel_normal(tickers,res,params,original=True)
    cor_plot(tickers,stock1,stock2,params,original=True)
    ########################################################################    

def res_hist_kernel_normal(tickers,res,params,original=True): 
    plt.rcParams['figure.figsize'] = (18.5, 10.5)
    norm = np.random.normal(loc=np.mean(res),scale=np.std(res),size=10000000)
    sns.distplot(norm,hist=False,kde_kws={"bw": 1, "label": "Normal"}) 
    sns.distplot(res,bins=100,kde_kws={"bw": 1, "label": "KDE(bw:1)"})
    sns.kdeplot(res, bw=.5, label="KDE(bw: 0.5)")
    sns.kdeplot(res, bw=.2, label="KDE(bw: 0.2)")
    plt.xlim(left=np.mean(res)-3*np.std(res),right=np.mean(res)+3*np.std(res))
    plt.ylim([0,1])
    plt.xlabel('value(in doller)',fontsize=30)
    plt.ylabel('frequency',fontsize=30)
    function=tickers[1]+'*'+str(round(float(params['m']),5))+'+'+str(round(float(params['b']),5))+'-'+tickers[0]
    plt.legend(fontsize=30)     
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30) 
    if original:
        plt.title('original residuals histogram('+function+')('+str(round(float(params['kurtosis']),5))+')',fontsize=30)
        plt.savefig(tickers[0]+'_'+tickers[1]+'_residuals histogram_original.png',dpi=1000)
        plt.close('all')
    else:
        plt.title('filtered residuals histogram('+function+')('+str(round(float(params['kurtosis']),5))+')',fontsize=30)
        plt.savefig(tickers[0]+'_'+tickers[1]+'_residuals histogram_filtered.png',dpi=1000)
        plt.close('all')

    
def cor_plot(tickers,stock1,stock2,params,original=True):
    plt.rcParams['figure.figsize'] = (18.5, 10.5)
    df_cor=pd.concat([stock1['close'],stock2['close']],axis=1)
    df_cor.columns=[tickers[0]+'_close',tickers[1]+'_close']  
    cor=df_cor.corr().iloc[1][0]
    sns.jointplot(x=tickers[0]+'_close', y=tickers[1]+'_close', data=df_cor, kind="reg",scatter_kws={"s": 1},line_kws={'color':'#00035b'})
    if original:
        plt.suptitle('original '+tickers[0]+' '+tickers[1]+' scatter plot(corr: '+str(round(cor,2))+')')
        plt.savefig(tickers[0]+'_'+tickers[1]+'_scatter plot_original.png',dpi=1000)
        plt.close('all')
    else:
        plt.suptitle('filtered '+tickers[0]+' '+tickers[1]+' scatter plot(corr: '+str(round(cor,2))+')')
        plt.savefig(tickers[0]+'_'+tickers[1]+'_scatter plot_filtered.png',dpi=1000)
        plt.close('all')
    
if __name__ == '__main__':
    import os
#    os.chdir('C:\\Users\\43739\\OneDrive\\US\\paper trading\\all_in_one\\v13')
    tickers = ['bp','rds-a'] 
    intra_freq = '1min'
    year='2018'
    params=statistic(tickers,intra_freq,year)    
    