# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 21:41:15 2019

@author: 43739
"""
import os
import pandas as pd
from datetime import datetime

# this file will create one year data from 2007 to 2018
# parameter
os.chdir('C:\\Users\\43739\\OneDrive\\us\\2019 spring\\paper trading')
auth_token = '****************************************'
tickers = ['bp','rds-a']
# name in variable_name is of no importance, just to nominate some dataframe 
variable_name=['BP','RDSA']
intra_freq = '1min'
#years=['2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007']
# 1min data from previous year is empty (before 2017)

years=['2018','2017']

for year in years:
    for ticker in tickers:
        # create data folder to download stock data to
        cur_dir = os.getcwd()
        foldername='data\\'+ticker+year
        data_dir = os.path.join(cur_dir, foldername)
        
        if not os.path.exists(data_dir):
            os.makedirs(foldername)
            
        # datelist
        # take 2018 as example(latest full year)
        def datelist(beginDate, endDate):
            date_l=[datetime.strftime(x,'%Y-%m-%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
            return date_l
        
        startdate=year+'-01-01'
        enddate=year+'-12-31'
        date_for_year=datelist(startdate, enddate)
        
        # create time list for download
        looplist=[]
        for x in range((int)(len(date_for_year)/5)):
            looplist.append(date_for_year[5*x])
            looplist.append(date_for_year[5*x+4])
         
        # download date based on time(don't have to run twice unless you delete the data)
        for x in range((int)(len(looplist)/2)):
            intra_start_date = looplist[(int)(x*2)]
            intra_end_date = looplist[(int)(x*2+1)]
            intra_url = f"https://api.tiingo.com/iex/{ticker}/prices?startDate={intra_start_date}&endDate={intra_end_date}&resampleFreq={intra_freq}&token={auth_token}"
            df_intra = pd.read_json(intra_url)
            intra_filepath = os.path.join(data_dir, f'intra_{ticker}_{intra_start_date}_{intra_end_date}_{intra_freq}.csv')
            df_intra.to_csv(intra_filepath)
        
        # merge
        first=pd.read_csv(data_dir+'\\intra_'+ticker+'_'+year+'-01-01_'+year+'-01-05_1min.csv',index_col=2)
        df_year = [first]
        df_year=pd.concat(df_year)
        for x in range(1,(int)(len(looplist)/2)):
            intra_start_date = looplist[(int)(x*2)]
            intra_end_date = looplist[(int)(x*2+1)]
            filename='data\\'+ticker+year+'\\intra_'+ticker+'_'+intra_start_date+'_'+intra_end_date+'_'+intra_freq+'.csv'
            if(os.path.getsize(filename)>4):
                temp=pd.read_csv(filename,index_col=2)
                df_year=[df_year,temp]
                df_year=pd.concat(df_year)
        # for data doesn't exit we just ignore them(empty csv is 4 bytes)
        
        # modify a bit
        df_year=df_year.drop(columns='Unnamed: 0')
        cols = list(df_year)
        cols.insert(0,cols.pop(cols.index('open')))
        cols.insert(1,cols.pop(cols.index('high')))
        cols.insert(2,cols.pop(cols.index('low')))
        df_year = df_year.loc[:,cols]
        
        #output csv
        outputname='data\\intra_'+ticker+'_'+year+'_'+intra_freq+'.csv'
        df_year.to_csv(outputname) 
        
    #match the date
    
    for i in range(len(tickers)):
        locals()[variable_name[i]]=pd.read_csv('data\\intra_'+tickers[i]+'_'+year+'_'+intra_freq+'.csv')
    
    A=locals()[variable_name[0]]
    for i in range(1,len(variable_name)):
        A=pd.merge(A,locals()[variable_name[i]],on="date")
    
    for i in range(len(variable_name)):
        locals()[variable_name[i]]=A.iloc[:,[0,4*i+1,4*i+2,4*i+3,4*i+4]]
        locals()[variable_name[i]].columns = ['date','open','high','low','close']
        name='data\\intra_'+tickers[i]+'_'+year+'_'+intra_freq+'.csv'
        locals()[variable_name[i]].to_csv(name,index=False)
