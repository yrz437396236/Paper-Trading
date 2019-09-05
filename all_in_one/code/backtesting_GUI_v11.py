# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:07:36 2019

@author: 43739
"""

from tkinter import *
from backtesting_main_v11 import core

def GUI():
    ##################################
    def run_core():
        core(auth_token=token_input.get(),tickers=[stock1_input.get(),stock2_input.get()]
        ,intra_freq=frequency_input.get(),year=year_input.get())
        process.set('Done')
##################################
    root = Tk()
    root.title('backtesting_v1.0')
    Label(root, text='Backtesting for pair trading',width=50,height=4).grid(row=0,column=0,columnspan=2)
    ##################################
#    auth_token = 'b2407b4b35df301601ad4fbb8c849f10c2ba1f21'
#    tickers = ['bp','rds-a'] 
#    intra_freq = '1min'
#    year='2018'
    ##################################
    Label(root, text='API Token :  ').grid(row=1,column=0)
    default_token=StringVar()    
    default_token.set(r'b2407b4b35df301601ad4fbb8c849f10c2ba1f21')
    token_input = Entry(root,textvariable=default_token,width=50)
    token_input.grid(row=1,column=1)
    ##################################
    Label(root, text='stock1 :  ').grid(row=2,column=0)
    default_stock1=StringVar()    
    default_stock1.set(r'bp')
    stock1_input = Entry(root,textvariable=default_stock1,width=10)
    stock1_input.grid(row=2,column=1)  
    ##################################
    Label(root, text='stock2 :  ').grid(row=3,column=0)
    default_stock2=StringVar()    
    default_stock2.set(r'rds-a')
    stock2_input = Entry(root,textvariable=default_stock2,width=10)
    stock2_input.grid(row=3,column=1) 
    ##################################
    Label(root, text='frequency :  ').grid(row=4,column=0)
    default_frequency=StringVar()    
    default_frequency.set(r'1min')
    frequency_input = Entry(root,textvariable=default_frequency,width=10)
    frequency_input.grid(row=4,column=1) 
    ##################################
    Label(root, text='year :  ').grid(row=5,column=0)
    default_year=StringVar()
    default_year.set(r'2018')
    year_input = Entry(root,textvariable=default_year)
    year_input.grid(row=5,column=1)  
    ##################################
    Label(root, text='===========================================').grid(row=6,column=0,columnspan=2)
    process=StringVar()
    process.set('start backtesting')
    Button(root, textvariable=process,command=run_core).grid(row=7,column=0,columnspan=2) 
    Label(root, text='v1.1').grid(row=8,column=2)
    mainloop()

if __name__ == '__main__':
    GUI()