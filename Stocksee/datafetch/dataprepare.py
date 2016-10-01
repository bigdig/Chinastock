# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 21:44:11 2016

@author: LT
"""

import pandas as pd
import os
import numpy as np
from datetime import datetime
import talib

def removeduplicate(infile='F:/chinesestock/day/000001.ss.csv',outfile='F:/chinesestock/day/000001.ss.csv'):
    data = pd.read_csv(infile,index_col='Date')
    
    data.loc[:,'Date'] = pd.to_datetime(data.index).map(lambda t: t.date().isoformat())
    data = data.drop_duplicates('Date',take_last=True).set_index('Date') #done!
    data.to_csv(outfile)
    
    
    return

def addfeature(infile='F:/chinesestock/day/000001.ss.csv',outfile='F:/chinesestock/day_feature/000001.ss.csv'):
    data = pd.read_csv(infile,index_col='Date')
    
    data = addfeature_basice(data)
    data = addfeature_MACD(data)
    data = addfeature_rollingmaxmin(data)
    data = addfeature_breakthrough(data)
    data = addfeature_train(data)
    #data = addfeature_pattern(data)
    data.to_csv(outfile)
    
    
    return 

def addfeature_basice(data):
    data.loc[:,'day_1_change_pct'] = data['Close'].diff() / data['Close'].shift() *100
    
    data.loc[:,'ischange_bigger_1'] = data['day_1_change_pct'].map(lambda t: 1 if t>1 else (-1 if t<-1 else 0))
    
    data.loc[:,'close_to_open'] = (data['Close'] / data['Open']-1)*100
    data.loc[:,'high_to_open'] = (data['High'] / data['Open']-1)*100
    data.loc[:,'low_to_open'] = (data['Low'] / data['Open']-1)*100
    data.loc[:,'day_1_change_tmr'] = data['day_1_change_pct'].shift(-1)
    data.loc[:,'ischange_bigger_1_tmr'] = data['day_1_change_tmr'].map(lambda t: 1 if t>1 else (-1 if t<-1 else 0))
    return data

def addfeature_MACD(data):
    macd, macdsignal, macdhist = talib.MACDFIX(data['Close'].values, signalperiod=9)
    #dataprepare =pd.DataFrame()
    data.loc[:,'macdhist'] = macdhist
    data.loc[:,'rollingsum_macdhist'] = pd.rolling_sum(data.macdhist,5)/100
    data.loc[:,'macdhist'] = data['macdhist'].map(lambda t: 1 if t>0 else 0)
    data.loc[:,'macdhist'] = pd.rolling_sum(data.macdhist,2)
    data.loc[:,'macdbuycross'] = 0
    data.loc[data.macdhist==1,'macdbuycross'] = 1
    data = data.drop(['macdhist'], 1)
    return data
def addfeature_breakthrough(data):
    
    #dataprepare =pd.DataFrame()
    data.loc[:,'1dayhighline'] = 2*data['High'].shift(1)-data['High'].shift(2)
    data.loc[:,'1daylowline'] = 2*data['Low'].shift(1)-data['Low'].shift(2)
    data.loc[:,'5dayhighline'] = data['High'].shift(1)+(data['High'].shift(1)-data['High'].shift(6))/5
    data.loc[:,'5daylowline'] = data['Low'].shift(1)+(data['Low'].shift(1)-data['Low'].shift(6))/5
    
    data.loc[:,'close_to_1dayhighline'] = data['Close']/data['1dayhighline']
    data.loc[:,'close_to_1daylowline'] = data['Close']/data['1daylowline']
    data.loc[:,'close_to_5dayhighline'] = data['Close']/data['5dayhighline']
    data.loc[:,'close_to_5daylowline'] = data['Close']/data['5daylowline']
    
    data = data.drop(['1dayhighline','1daylowline','5dayhighline','5daylowline'], 1)
    return data    
def addfeature_rollingmaxmin(data):
    
    #dataprepare =pd.DataFrame()


    data.loc[:,'rollingmax30'] = pd.rolling_max(data['High'],30)
    data.loc[:,'close_to_rollingmax30'] = data['Close']/data['rollingmax30']
    data.loc[:,'rollingmax10'] = pd.rolling_max(data['High'],10)
    data.loc[:,'close_to_rollingmax10'] = data['Close']/data['rollingmax10']
    data.loc[:,'rollingmax5'] = pd.rolling_max(data['High'],5)
    data.loc[:,'close_to_rollingmax5'] = data['Close']/data['rollingmax5']
    data.loc[:,'rollingmin30'] = pd.rolling_max(data['Low'],30)
    data.loc[:,'close_to_rollingmin30'] = data['Close']/data['rollingmin30']
    data.loc[:,'rollingmin10'] = pd.rolling_max(data['Low'],10)
    data.loc[:,'close_to_rollingmin10'] = data['Close']/data['rollingmin10']
    data.loc[:,'rollingmin5'] = pd.rolling_max(data['Low'],5)
    data.loc[:,'close_to_rollingmin5'] = data['Close']/data['rollingmin5']
    data = data.drop(['rollingmax30','rollingmax10','rollingmax5','rollingmin30','rollingmin10','rollingmin5'], 1)
    return data
def addfeature_train(data):
    
    for i in range(1,4):    
        data.loc[:,'close_to_open_yesterday-'+str(i)] = data['close_to_open'].shift(i)
        data.loc[:,'high_to_open_yesterday-'+str(i)] = data['high_to_open'].shift(i)
        data.loc[:,'low_to_open_yesterday-'+str(i)] = data['low_to_open'].shift(i)
        data.loc[:,'day_1_change_pct_yesterday-'+str(i)]= data['day_1_change_pct'].shift(i)
    data.loc[:,'MA5'] = pd.rolling_mean(data['Close'],window=5)    
    data.loc[:,'MA10'] = pd.rolling_mean(data['Close'],window=10)
    data.loc[:,'MA30'] = pd.rolling_mean(data['Close'],window=30)
    data.loc[:,'MA60'] = pd.rolling_mean(data['Close'],window=60)
    data.loc[:,'close_to_MA5'] = (data['Close']/data['MA5']-1)*100
    data.loc[:,'high_to_MA5'] = (data['High']/data['MA5']-1)*100
    data.loc[:,'low_to_MA5'] = (data['Low']/data['MA5']-1)*100
    data.loc[:,'MA5_to_MA10'] = (data['MA5']/data['MA10']-1)*100
    data.loc[:,'close_to_MA10'] = (data['Close']/data['MA10']-1)*100
    data.loc[:,'high_to_MA10'] = (data['High']/data['MA10']-1)*100
    data.loc[:,'low_to_MA10'] = (data['Low']/data['MA10']-1)*100
    data.loc[:,'MA10_to_MA30'] = (data['MA10']/data['MA30']-1)*100
    data.loc[:,'MA30_to_MA60'] = (data['MA30']/data['MA60']-1)*100
    data.loc[:,'MA5trend'] = (data['MA5'] / data['MA5'].shift(5)-1) *100
    data.loc[:,'MA10trend'] = (data['MA10'] / data['MA10'].shift(10)-1) *100
    data.loc[:,'MA30trend'] = (data['MA30'] / data['MA30'].shift(30)-1) *100
    data.loc[:,'MA60trend'] = (data['MA60'] / data['MA60'].shift(60)-1) *100
    data = data.drop(['MA5','MA10','MA30','MA60'], 1)
    return data
    
def addfeature_pattern(data):
    data.loc[:,'CDL2CROWS'] = talib.CDL2CROWS(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDL3BLACKCROWS'] = talib.CDL3BLACKCROWS(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDL3INSIDE'] = talib.CDL3INSIDE(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDL3LINESTRIKE'] = talib.CDL3LINESTRIKE(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDL3OUTSIDE'] = talib.CDL3OUTSIDE(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDL3STARSINSOUTH'] = talib.CDL3STARSINSOUTH(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDL3WHITESOLDIERS'] = talib.CDL3WHITESOLDIERS(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLABANDONEDBABY'] = talib.CDLABANDONEDBABY(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLADVANCEBLOCK'] = talib.CDLADVANCEBLOCK(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLBELTHOLD'] = talib.CDLBELTHOLD(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLBREAKAWAY'] = talib.CDLBREAKAWAY(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLCLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLCONCEALBABYSWALL'] = talib.CDLCONCEALBABYSWALL(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLCOUNTERATTACK'] = talib.CDLCOUNTERATTACK(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLDARKCLOUDCOVER'] = talib.CDLDARKCLOUDCOVER(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLDOJI'] = talib.CDLDOJI(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100 
    data.loc[:,'CDLDOJISTAR'] = talib.CDLDOJISTAR(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLDRAGONFLYDOJI'] = talib.CDLDRAGONFLYDOJI(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLENGULFING'] = talib.CDLENGULFING(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLEVENINGDOJISTAR'] = talib.CDLEVENINGDOJISTAR(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLEVENINGSTAR'] = talib.CDLEVENINGSTAR(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLGAPSIDESIDEWHITE'] = talib.CDLGAPSIDESIDEWHITE(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLGRAVESTONEDOJI'] = talib.CDLGRAVESTONEDOJI(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100    
    data.loc[:,'CDLHAMMER'] = talib.CDLHAMMER(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLHANGINGMAN'] = talib.CDLHANGINGMAN(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLHARAMI'] = talib.CDLHARAMI(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLHARAMICROSS'] = talib.CDLHARAMICROSS(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLHIGHWAVE'] = talib.CDLHIGHWAVE(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLHIKKAKE'] = talib.CDLHIKKAKE(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLHIKKAKEMOD'] = talib.CDLHIKKAKEMOD(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLHOMINGPIGEON'] = talib.CDLHOMINGPIGEON(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLIDENTICAL3CROWS'] = talib.CDLIDENTICAL3CROWS(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLINNECK'] = talib.CDLINNECK(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values) /100   
    data.loc[:,'CDLINVERTEDHAMMER'] = talib.CDLINVERTEDHAMMER(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLKICKING'] = talib.CDLKICKING(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLKICKINGBYLENGTH'] = talib.CDLKICKINGBYLENGTH(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100    
    data.loc[:,'CDLLADDERBOTTOM'] = talib.CDLLADDERBOTTOM(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLLONGLINE'] = talib.CDLLONGLINE(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLMARUBOZU'] = talib.CDLMARUBOZU(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLMATCHINGLOW'] = talib.CDLMATCHINGLOW(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLMATHOLD'] = talib.CDLMATHOLD(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLMORNINGDOJISTAR'] = talib.CDLMORNINGDOJISTAR(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLMORNINGSTAR'] = talib.CDLMORNINGSTAR(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLONNECK'] = talib.CDLONNECK(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLPIERCING'] = talib.CDLPIERCING(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100  
    data.loc[:,'CDLRICKSHAWMAN'] = talib.CDLRICKSHAWMAN(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLRISEFALL3METHODS'] = talib.CDLRISEFALL3METHODS(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLSEPARATINGLINES'] = talib.CDLSEPARATINGLINES(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLSHOOTINGSTAR'] = talib.CDLSHOOTINGSTAR(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLSHORTLINE'] = talib.CDLSHORTLINE(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLSPINNINGTOP'] = talib.CDLSPINNINGTOP(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLSTALLEDPATTERN'] = talib.CDLSTALLEDPATTERN(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLSTICKSANDWICH'] = talib.CDLSTICKSANDWICH(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLTAKURI'] = talib.CDLTAKURI(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLTASUKIGAP'] = talib.CDLTASUKIGAP(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLTHRUSTING'] = talib.CDLTHRUSTING(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLTRISTAR'] = talib.CDLTRISTAR(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLUNIQUE3RIVER'] = talib.CDLUNIQUE3RIVER(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    data.loc[:,'CDLUPSIDEGAP2CROWS'] = talib.CDLUPSIDEGAP2CROWS(data['Open'].values,data['High'].values,data['Low'].values,data['Close'].values)/100
    
    
    
    return data    

def addfeature_all(infolder='F:/chinesestock/day/',outfolder='F:/chinesestock/day_feature/',func= 'addfeature'):
    if not os.path.exists(infolder):
        os.makedirs(infolder)
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)         
    for file in os.listdir(infolder): 
        print 'add feature for %s ' % file
        usefunc = globals()[func]         
        usefunc(infolder+file,outfolder+file)    
    return 

def generatecorrelation(infolder='F:/chinesestock/day_feature/',outfile='F:/chinesestock/anlysis/correlation.csv',start=0,
                        observe = 'day_1_change_pct',predict = 'day_1_change_tmr'):
        
    observes = pd.DataFrame()
    predicts = pd.DataFrame()
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        observes.loc[:,file[0:6]] = newdata[observe]
        predicts.loc[:,file[0:6]] = newdata[predict]
    
    correlation = pd.DataFrame(index = observes.columns,columns=predicts.columns) 
    for todayticker in observes.columns:
        print 'correlation for %s ' % todayticker
        for tmrticker in predicts.columns:
            todaytmr = pd.DataFrame()
            todaytmr.loc[:,"t"] = observes[todayticker]
            todaytmr.loc[:,"t+1"] = predicts[tmrticker]
            todaytmr =todaytmr.dropna()
            todaytmr = todaytmr.ix[-start:]
            correlation.loc[todayticker,tmrticker] = todaytmr.corr().ix[0,1]
    
    correlation.to_csv(outfile)
    
    
    return
def generateprobability(infolder='F:/chinesestock/day_feature/',outfolder='F:/chinesestock/anlysis/',
                        observe = 'ischange_bigger_1',predict = 'ischange_bigger_1_tmr'):
        
    observes = pd.DataFrame()
    predicts = pd.DataFrame()
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        observes.loc[:,file[0:6]] = newdata[observe]
        predicts.loc[:,file[0:6]] = newdata[predict]
    
    correlation100 = pd.DataFrame(index = observes.columns,columns=predicts.columns) 
    correlation30 = pd.DataFrame(index = observes.columns,columns=predicts.columns)
    correlation10 = pd.DataFrame(index = observes.columns,columns=predicts.columns)
    for todayticker in observes.columns:
        print 'probability for %s ' % todayticker
        for tmrticker in predicts.columns:
            todaytmr = pd.DataFrame()
            todaytmr.loc[:,"t"] = observes[todayticker]
            todaytmr.loc[:,"t+1"] = predicts[tmrticker]
            todaytmr =todaytmr.dropna()
            todaytmr100 = todaytmr.ix[-100:]    
            todaytmr30 = todaytmr.ix[-30:]  
            todaytmr10 = todaytmr.ix[-10:] 
            correlation100.loc[todayticker,tmrticker] = todaytmr100.loc[todaytmr100.t==1,'t+1'].mean()
            correlation30.loc[todayticker,tmrticker] = todaytmr30.loc[todaytmr30.t==1,'t+1'].mean()
            correlation10.loc[todayticker,tmrticker] = todaytmr10.loc[todaytmr10.t==1,'t+1'].mean()
    correlation100.to_csv(outfolder+'probability_recent100.csv')
    correlation30.to_csv(outfolder+'probability_recent30.csv')
    correlation10.to_csv(outfolder+'probability_recent10.csv')
    
    return    
def generatecorrelation_sameday(infolder='F:/chinesestock/day_feature/',outfile='F:/chinesestock/anlysis/correlation_.csv',start=0):
        
    today_change = pd.DataFrame()
    
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        today_change.loc[:,file[0:6]] = newdata['day_1_change_pct']
        
    
    correlation = pd.DataFrame(index = today_change.columns,columns=today_change.columns) 
    for todayticker in today_change.columns:
        print 'correlation for %s ' % todayticker
        for tmrticker in today_change.columns:
            todaytmr = pd.DataFrame()
            todaytmr.loc[:,"t"] = today_change[todayticker]
            todaytmr.loc[:,"t+1"] = today_change[tmrticker]
            todaytmr =todaytmr.dropna()
            todaytmr = todaytmr.ix[-start:]
            correlation.loc[todayticker,tmrticker] = todaytmr.corr().ix[0,1]
    
    correlation.to_csv(outfile)
    
    
    return
    
def generate_trainfile(infolder='F:/chinesestock/day_feature/',outfile='F:/chinesestock/anlysis/train.csv',start=-600):
    
    traindata = pd.DataFrame()
    
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        
        newdata = newdata.drop(['Open','High','Low','Close','Volume','Adj Close'], 1)
        newdata = newdata.ix[-start:]  
        newdata.loc[:,'sampleweight'] = range(len(newdata.index))
        traindata = traindata.append(newdata, ignore_index=True)
 
    
    traindata.to_csv(outfile)
    
    
    return 

def doall():
    addfeature_all()
    generateprobability()
    
    generatecorrelation(outfile='F:/chinesestock/anlysis/correlation_recent20.csv',start=20)
    generatecorrelation(outfile='F:/chinesestock/anlysis/correlation_recent100.csv',start=100)

    return    
    
if __name__ == '__main__':
    addfeature_all()
    
    generate_trainfile()



    #addfeature_all(infolder='F:/chinesestock/day/',outfolder='F:/chinesestock/day/',func='removeduplicate')
    #removeduplicate()
    #generatecorrelation_sameday()
    #addfeature()
    #generatecorrelation(outfile='F:/chinesestock/anlysis/correlation_recent100.csv',start=100)
    #generatecorrelation_sameday(outfile='F:/chinesestock/anlysis/correlation_sameday__recent100.csv',start=100)
    '''
    generatecorrelation_sameday(outfile='F:/chinesestock/anlysis/correlation_sameday__recent30.csv',start=30)
    generatecorrelation_sameday(outfile='F:/chinesestock/anlysis/correlation_sameday__recent20.csv',start=20)
    generatecorrelation_sameday(outfile='F:/chinesestock/anlysis/correlation_sameday__recent10.csv',start=10)
    generatecorrelation_sameday(outfile='F:/chinesestock/anlysis/correlation_sameday__recent5.csv',start=5)
    generatecorrelation(outfile='F:/chinesestock/anlysis/correlation_recent20.csv',start=20)
     
    generatecorrelation(outfile='F:/chinesestock/anlysis/correlation_recent10.csv',start=10)
    generatecorrelation(outfile='F:/chinesestock/anlysis/correlation_recent30.csv',start=30)
    '''
    #doall()
    #generatecorrelation(outfile='F:/chinesestock/anlysis/correlation_recent20.csv',start=20)