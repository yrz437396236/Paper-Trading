# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:22:45 2019

@author: 43739
"""
import pandas as pd
import datetime
from dateutil.tz import tzstr

def delete_abrupt_time(original):
    NY_time=[(x-datetime.timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S") for x in [datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S") for x in original.index.tolist()]]
    # minus four hour to convert it to New York time
    original.index=NY_time
    date=pd.Series([x[0:10] for x in original.index],index=original.index)
    time=pd.Series([x[11::] for x in original.index],index=original.index)
    tz = tzstr('EST+5EDT,M3.2.0,M11.1.0')#http://famschmid.net/timezones.html
    timezones=[datetime.datetime(int(date[x][0:4]),int(date[x][5:7]),int(date[x][8:10]), 0, 0, tzinfo=tz).tzname() for x in range(len(date))]
    def abrupt_time_finder(timezones,time):
        abrupt_time=[False]*len(date)
        for index,timezone in enumerate(timezones):
            if timezone =='EDT':
                if time[index][0:2]=='09':
                    abrupt_time[index]=True
                elif time[index][0:2]=='15':
                    if int(time[index][3:5])>30:
                        abrupt_time[index]=True
                elif time[index][0:2]=='16':
                    abrupt_time[index]=True                
                else:
                    pass
            else:
                if time[index][0:2]=='10':
                    abrupt_time[index]=True
                elif time[index][0:2]=='16':
                    if int(time[index][3:5])>30:
                        abrupt_time[index]=True
                elif time[index][0:2]=='17':
                    abrupt_time[index]=True            
                else:
                    pass
        return abrupt_time
    abrupt_time=pd.Series(abrupt_time_finder(timezones,time),index=original.index)
    original=pd.concat([original,abrupt_time],axis=1)
    original.columns=['open','high','low','close','abrupt_time']
    cooked=original[original['abrupt_time'].values==False][['open','high','low','close']]
    return cooked

if __name__ == '__main__':
    original=pd.read_csv('data//intra_aapl_2018_1min.csv',index_col=0)
    cooked=delete_abrupt_time(original)
