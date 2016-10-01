# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 18:36:36 2016

@author: LT
"""

import pandas as pd
from pandas.io.data import DataReader
import os

from datetime import datetime

def yahoofinance_get(datafolder='F:/chinesestock/day/',startdate="2010-01-21",enddate =datetime.today().date().isoformat()):
    tickerlist = pd.read_csv(os.path.join(os.path.abspath(os.pardir),"config/sh_stocklist.csv"))
    tickerlist = tickerlist.loc[:,'ticker'].values.tolist()    
    for ticker in tickerlist:
        print 'Downloading data from Yahoo for %s ' % ticker
        try:
            filename = datafolder+ticker+'.csv'                
            data = DataReader(ticker, 'yahoo', startdate)         
            data.to_csv(filename)
        except IOError:
            print 'Someproblem wiht downloading for %s ' % ticker
        
    print 'Finished downloading data'
    
    configfile = os.path.join(os.path.abspath(os.pardir),"config/record.csv")
    configs = pd.read_csv(configfile,index_col='index')
    configs.loc['yahoorefreshday','value'] = enddate
    configs.to_csv(configfile)
    
    return
    
def yahoofinance_refresh(datafolder='F:/chinesestock/day/',origindate="2010-01-21",enddate =datetime.today().date().isoformat()):
    #configs = pd.read_csv(os.path.join(os.path.abspath(os.pardir),"config/record.csv"),index_col='index')
    configfile = "F:/Stocksee/config/record.csv"
    configs = pd.read_csv(configfile,index_col='index')
    startdate = configs.loc['yahoorefreshday','value']
    #tickerlist = pd.read_csv(os.path.join(os.path.abspath(os.pardir),"config/sh_stocklist.csv"))
    tickerlist = pd.read_csv("F:/Stocksee/config/sh_stocklist.csv")
    tickerlist = tickerlist.loc[:,'ticker'].values.tolist()    
    for ticker in tickerlist:
        print 'Downloading data from Yahoo for %s ' % ticker
        try:
            filename = datafolder+ticker+'.csv'
            if os.path.exists(filename):
                data = pd.read_csv(filename,index_col='Date')                               
                newdata = DataReader(ticker, 'yahoo', startdate)
                newdata.index = newdata.index.map(lambda t: t.date().isoformat())
                data = pd.concat([data,newdata])
            else:                
                data = DataReader(ticker, 'yahoo', origindate,enddate)         
            data.loc[:,'Date'] = pd.to_datetime(data.index).map(lambda t: t.date().isoformat())
            data = data.drop_duplicates('Date',take_last=True).set_index('Date') #done!
    
            data.to_csv(filename)
        except IOError:
            print 'Someproblem wiht downloading for %s ' % ticker
        
    print 'Finished downloading data'
    
    #configfile = os.path.join(os.path.abspath(os.pardir),"config/record.csv")
    
    configs = pd.read_csv(configfile,index_col='index')
    configs.loc['yahoorefreshday','value'] = enddate
    configs.to_csv(configfile)
    
    return
   

if __name__ == '__main__':
    
    #yahoofinance_get()
    
    yahoofinance_refresh()