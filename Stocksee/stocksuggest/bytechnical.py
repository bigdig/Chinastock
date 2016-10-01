# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 21:23:22 2016

@author: LT
"""

import pandas as pd
import os
import numpy as np
from datetime import datetime,date



def suggestbyMACD(workfolder='F:/chinesestock/', threshhold=0.8,
                         anlysisfilename='probability_MACD.csv'):
    #step1,get MACD
    
    observes = pd.DataFrame()
    infolder = workfolder + 'day_feature/'
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        observes.loc[:,file[0:6]] = newdata['macdhist']
    
    #get column with last macd>0
    observes = observes.iloc[-20:]
    observes = observes.loc[:,observes.iloc[-1]>0]
    observes = observes.loc[:,(observes.iloc[-5:]<0).any()]
    suggest = pd.DataFrame(observes.sum(axis=0),index = observes.columns,columns=['macd_sum'])
    
    #save file
    outfolder =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/'
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outfile = outfolder + anlysisfilename
    suggest = suggest.sort(columns ='macd_sum' )
    suggest.to_csv(outfile)
    
    
    return
    
    
    
if __name__ == '__main__':
    
    suggestbyMACD() 