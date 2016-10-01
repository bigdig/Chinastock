# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 16:44:11 2016

@author: LT
"""
import pandas as pd
import os
import numpy as np
from datetime import datetime,date


def suggestbyprobability(workfolder='F:/chinesestock/', threshhold=0.8,
                         anlysisfilename='probability_recent30.csv'):
    #step1,get stock move
    
    observes = pd.DataFrame()
    infolder = workfolder + 'day_feature/'
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        observes.loc[:,file[0:6]] = newdata['ischange_bigger_1']
    observes = observes.ix[-1]
    #get analysis
    anlysisfile = workfolder + 'anlysis/'+anlysisfilename
    correlation = pd.read_csv(anlysisfile,index_col=0)
    correlation = correlation.applymap(lambda t: t if t>threshhold else 0)
    result = pd.DataFrame(columns=correlation.columns ,index = correlation.index)
    result = correlation.apply(lambda t: np.asarray(t) * np.asarray(observes),axis=1)
    suggest = result.sum(axis=0)
    suggest.sort(ascending=False)
    #save file
    outfolder =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/'
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outfile = outfolder + anlysisfilename
    suggest = suggest[suggest>0]
    suggest.to_csv(outfile)
    
    
    return
  
def whatIwant(workfolder='F:/chinesestock/'):
    thefile =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/correlation_recent100.csv'
    data = pd.read_csv(thefile,header=None,index_col=0)
    
    newfile =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/correlation_recent20.csv'
    newdata = pd.read_csv(newfile,header=None,index_col=0)
    data.loc[:,'corr_recent20']=newdata    
    
    newfile =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/probability_recent100.csv'
    newdata = pd.read_csv(newfile,header=None,index_col=0)
    data.loc[:,'recent100']=newdata
    
    newfile =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/probability_recent30.csv'
    newdata = pd.read_csv(newfile,header=None,index_col=0)
    data.loc[:,'recent30']=newdata
    newfile =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/probability_recent10.csv'
    newdata = pd.read_csv(newfile,header=None,index_col=0)
    data.loc[:,'recent10']=newdata
    outfile = workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/whatIwant.csv'
    data.to_csv(outfile)
    
    return
    
if __name__ == '__main__':
    
    suggestbyprobability()    
    suggestbyprobability(anlysisfilename='probability_recent10.csv')
    suggestbyprobability(anlysisfilename='probability_recent100.csv')
    suggestbyprobability(anlysisfilename='correlation_recent20.csv', threshhold=0.8)
    suggestbyprobability(anlysisfilename='correlation_recent100.csv', threshhold=0.8)
    
    whatIwant()
    
    suggestbyprobability(anlysisfilename='correlation_recent100.csv', threshhold=0.8)
    