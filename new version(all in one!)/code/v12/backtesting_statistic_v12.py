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

def statistic(tickers,intra_freq,year):
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
    ########################################################################
    #statistic plots
    res_hist_kernel_normal(tickers,res,params)
    cor_plot(tickers,stock1,stock2,params)
    ########################################################################
    return params

def res_hist_kernel_normal(tickers,res,params): 
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
    plt.title('residuals histogram('+function+')',fontsize=30)
    plt.legend(fontsize=30)     
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)   
    plt.savefig(tickers[0]+'_'+tickers[1]+'_residuals histogram.png',dpi=1000)
    
def cor_plot(tickers,stock1,stock2,params):
    plt.rcParams['figure.figsize'] = (18.5, 10.5)
    df_cor=pd.concat([stock1['close'],stock2['close']],axis=1)
    df_cor.columns=[tickers[0]+'_close',tickers[1]+'_close']  
    cor=df_cor.corr().iloc[1][0]
    sns.jointplot(x=tickers[0]+'_close', y=tickers[1]+'_close', data=df_cor, kind="reg",scatter_kws={"s": 1},line_kws={'color':'#00035b'})
    plt.suptitle(tickers[0]+' '+tickers[1]+' scatter plot(corr: '+str(round(cor,2))+')')
    plt.savefig(tickers[0]+'_'+tickers[1]+'_scatter plot.png',dpi=1000)
    
if __name__ == '__main__':
    import os
    os.chdir('D:\\test\\all_in_one\\v12')
    tickers = ['bp','rds-a'] 
    intra_freq = '1min'
    year='2018'
    params=statistic(tickers,intra_freq,year)    
    