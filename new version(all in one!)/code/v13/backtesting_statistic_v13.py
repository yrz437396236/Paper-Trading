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
from scipy.stats import kurtosis,norm

def statistic(tickers,intra_freq,year):
    stock1_original=pd.read_csv('data\\intra_'+tickers[0]+'_'+year+'_'+intra_freq+'.csv',index_col=0)
    stock2_original=pd.read_csv('data\\intra_'+tickers[1]+'_'+year+'_'+intra_freq+'.csv',index_col=0)
    stock1_filtered=delete_abrupt_time(stock1_original)
    stock2_filtered=delete_abrupt_time(stock2_original)
    stock1_filtered.to_csv('data\\intra_'+tickers[0]+'_'+year+'_'+intra_freq+'_filtered.csv')
    stock2_filtered.to_csv('data\\intra_'+tickers[1]+'_'+year+'_'+intra_freq+'_filtered.csv')
    close1=stock1_filtered['close'].values.reshape(-1, 1)
    close2=stock2_filtered['close'].values.reshape(-1, 1)
    reg=LinearRegression().fit(close2, close1)
    slope=reg.coef_[0][0]
    intercept=reg.intercept_[0] 
    res=stock2_filtered['close'].values*slope+intercept-stock1_filtered['close'].values
    std=np.std(res)
    params={'m':slope,'b':intercept,'std':std,'avg':0.5,'muti':1,'size':1000}
    ########################################################################
    #statistic plots
    res_hist_kernel_normal(tickers,res,params)
    cor_plot(tickers,stock1_filtered,stock2_filtered,params)
    daily_std_plot(tickers,stock1_original,stock2_original,stock1_filtered,stock2_filtered,params,year)
    ########################################################################
    return params

def daily_std_plot(tickers,stock1_original,stock2_original,stock1_filtered,stock2_filtered,params,year):
    datelist_original=pd.Series([x[0:10] for x in stock1_original.index],index=stock1_original.index)
    datelist_filtered=pd.Series([x[0:10] for x in stock1_filtered.index],index=stock1_filtered.index)    
    stock1_original=pd.concat([stock1_original,datelist_original],axis=1)
    stock2_original=pd.concat([stock2_original,datelist_original],axis=1)
    stock1_filtered=pd.concat([stock1_filtered,datelist_filtered],axis=1)
    stock2_filtered=pd.concat([stock2_filtered,datelist_filtered],axis=1) 
    datelist_unique=sorted(list(set([x[0:10] for x in stock1_original.index.tolist()])))
    #same for two stocks since we pair the date when download and merge data
    std_dict={}
    original_res_diff_yearly=[]
    filtered_res_diff_yearly=[]
    for i in datelist_unique:           
        original_res_daily=stock2_original[stock2_original[0]==i]['close'].values*params['m']+params['b']-stock1_original[stock1_original[0]==i]['close'].values
        filtered_res_daily=stock2_filtered[stock2_filtered[0]==i]['close'].values*params['m']+params['b']-stock1_filtered[stock1_filtered[0]==i]['close'].values
        original_res_diff_yearly=original_res_diff_yearly+np.diff(original_res_daily).tolist()
        filtered_res_diff_yearly=filtered_res_diff_yearly+np.diff(filtered_res_daily).tolist()
        std_dict[i]=[np.std(original_res_daily)-np.std(filtered_res_daily)] 
    daily_std=pd.DataFrame(std_dict).T
    daily_std.columns=['original-filtered']
    daily_std['date']=daily_std.index
    daily_std['original-filtered'].std()
    quarter=len(daily_std['date'])//4
    xticks_list=[daily_std['date'][0],daily_std['date'][quarter],daily_std['date'][quarter*2],daily_std['date'][quarter*3],daily_std['date'][quarter*4]]
    ########################################################################
    plt.rcParams['figure.figsize'] = (18.5, 10.5)
    plt.plot(daily_std['date'],daily_std['original-filtered'])
    plt.xlabel('date',fontsize=30)
    plt.ylabel('diff',fontsize=30)
    plt.title('Original minus Filtered',fontsize=30)
    plt.legend(fontsize=30) 
    plt.xticks(xticks_list,fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig(tickers[0]+'_'+tickers[1]+'_Original minus filtered.png',dpi=1000)
    plt.close('all')
    ########################################################################
    sns.set(font_scale=2)
    plt.rcParams['figure.figsize'] = (18.5, 18.5)
    fig,axes=plt.subplots(2,1)
    sns.distplot(original_res_diff_yearly,norm_hist=True, bins=200,fit=norm,ax=axes[0])
    axes[0].set_title('Original(std : '+str(round(np.std(original_res_diff_yearly),5))+')',fontsize=30)
    sns.distplot(filtered_res_diff_yearly,norm_hist=True, bins=200,fit=norm,ax=axes[1])
    axes[1].set_title('Filtered(std : '+str(round(np.std(filtered_res_diff_yearly),5))+')',fontsize=30)
    plt.suptitle('Residual diff histogram',fontsize=30)
    plt.savefig(tickers[0]+'_'+tickers[1]+'_Residual diff histogram.png',dpi=1000)
    plt.close('all')
    
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
    plt.title('Residual histogram('+function+')',fontsize=30)
    plt.legend(fontsize=30)     
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)   
    plt.savefig(tickers[0]+'_'+tickers[1]+'_Residual histogram.png',dpi=1000)
    plt.close('all')
    
def cor_plot(tickers,stock1_filtered,stock2_filtered,params):
    sns.set(font_scale=1)
    plt.rcParams['figure.figsize'] = (18.5, 10.5)
    df_cor=pd.concat([stock1_filtered['close'],stock2_filtered['close']],axis=1)
    df_cor.columns=[tickers[0]+'_close',tickers[1]+'_close']  
    cor=df_cor.corr().iloc[1][0]
    sns.jointplot(x=tickers[0]+'_close', y=tickers[1]+'_close', data=df_cor, kind="reg",scatter_kws={"s": 1},line_kws={'color':'#00035b'})
    plt.suptitle(tickers[0]+' '+tickers[1]+'Scatter plot(corr: '+str(round(cor,2))+')')
    plt.savefig(tickers[0]+'_'+tickers[1]+'_Scatter plot.png',dpi=1000)
    plt.close('all')
    
if __name__ == '__main__':
    tickers = ['bp','rds-a'] 
    intra_freq = '1min'
    year='2018'
    params=statistic(tickers,intra_freq,year)    
    