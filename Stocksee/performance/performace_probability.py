# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 14:47:08 2016

@author: LT
"""

import pandas as pd
import os
from datetime import datetime


def add_performance(workfolder='F:/chinesestock/'):
    #read top day percent change
    
    observes = pd.DataFrame()
    infolder = workfolder+'day_feature/'
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        newdata = newdata.iloc[-1]
        observes.loc[file[0:6],'performance'] = newdata['day_1_change_pct']
    
     
    #read last day predict
    folder = pd.Series(os.listdir(workfolder+'stocksuggest/'))
    folder.sort()                    
    lastday = folder.values[-1]
    infolder = workfolder+'stocksuggest/'+lastday+'/'
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        if file=="whatIwant.csv":
            newdata = pd.read_csv(infolder+file,header=0,index_col=0)
        else:
            newdata = pd.read_csv(infolder+file,header=None,index_col=0)
        newdata.index = newdata.index.map(lambda t: str(t)[0:6])
        
        newdata = newdata.merge(observes,how='left',left_index=True,right_index=True)
        newdata.to_csv(infolder+file)
        

if __name__ == '__main__':
    add_performance()
    
    