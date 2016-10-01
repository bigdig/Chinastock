# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 16:19:59 2016

@author: LT
"""

import pandas as pd
import os
import numpy as np
from datetime import datetime,date
from sklearn.svm import SVC,LinearSVC
from sklearn import tree
import pandas as pd
import os
import pickle
from sklearn.ensemble import RandomForestClassifier
#from sklearn.neural_network import MLPClassifier


def MLPfromfile(workfolder='F:/chinesestock/anlysis/'):
    data = pd.read_csv(workfolder+'train.csv',index_col=0).dropna()

    X = data.drop(['ischange_bigger_1_tmr','day_1_change_tmr'], 1)
    Y = data['ischange_bigger_1_tmr'] 

    clf1 = MLPClassifier()
    
    clf1.fit(X, Y)
      
    print clf1.score(X,Y)
    pickle.dump( clf1, open( workfolder+"MLP.p", "wb" ) )
    return


def SVMfromfile(workfolder='F:/chinesestock/anlysis/'):
    data = pd.read_csv(workfolder+'train.csv',index_col=0).dropna()

    X = data.drop(['ischange_bigger_1_tmr','day_1_change_tmr'], 1)
    Y = data['ischange_bigger_1_tmr'] 

    clf1 = LinearSVC() #svc tried, cant get a result
    
    clf1.fit(X, Y)
      
    print clf1.score(X,Y)
    pickle.dump( clf1, open( workfolder+"SVC.p", "wb" ) )
    return 


def suggestbySVC(workfolder='F:/chinesestock/',
                         anlysisfilename='SVC.p'):
    #read analysis file
    analysisfile = workfolder + 'anlysis/' + anlysisfilename             
    machine = pickle.load( open( analysisfile, "rb" ) )
    
    
    observes = {}
    infolder = workfolder + 'day_feature/'
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        newdata = newdata.drop(['Open','High','Low','Close','Volume','Adj Close','ischange_bigger_1_tmr','day_1_change_tmr'], 1)
        newdata = newdata.ix[-1].dropna()
        signal = 0
        try:
            signal = machine.predict(newdata)
        except:
            pass
        if signal == 1:
            print 'find signal in %s' % file
            score = 0
            try:
                score = machine.decision_function(newdata)
            except:
                pass
            observes[file[0:6]]=score
    
    suggest = pd.DataFrame(observes).transpose()
    
    #save file
    outfolder =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/'
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outfile = outfolder + anlysisfilename + '.csv'
    
    suggest.to_csv(outfile)
    
def Treefromfile(workfolder='F:/chinesestock/anlysis/'):
    data = pd.read_csv(workfolder+'train.csv',index_col=0).dropna()
    data = data.applymap(lambda t: 10 if t>10 else (-10 if t<-10 else t))
    Y1 = data['day_1_change_tmr'].map(lambda t: 1 if t>2 else (-1 if t<-1 else 0))
    sample_weight = data['sampleweight'].tolist()
    sample_weight = np.array(sample_weight)
    X = data.drop(['ischange_bigger_1_tmr','day_1_change_tmr','sampleweight'], 1)
    Y = data['ischange_bigger_1_tmr'] 

    #clf1 = tree.DecisionTreeClassifier(class_weight={0:.9, 1:.1}) # 1 is what I wish to have
    clf1 = RandomForestClassifier(n_estimators=30)
    clf1.fit(X, Y,sample_weight=sample_weight)   
    pickle.dump( clf1, open( workfolder+"Tree.p", "wb" ) )
    clf2 = RandomForestClassifier(n_estimators=30)
    clf2.fit(X, Y1,sample_weight=sample_weight)   
    pickle.dump( clf2, open( workfolder+"Tree2.p", "wb" ) )
    return
    
    
def suggestbyTree(workfolder='F:/chinesestock/',
                         anlysisfilename='Tree.p'):
    #read analysis file
    analysisfile = workfolder + 'anlysis/' + anlysisfilename             
    machine = pickle.load( open( analysisfile, "rb" ) )
    
    
    
    global observes
    observes = {}
    infolder = workfolder + 'day_feature/'
    for file in os.listdir(infolder):
        print 'read data from %s ' % file
        newdata = pd.read_csv(infolder+file,index_col='Date')
        newdata = newdata.drop(['Open','High','Low','Close','Volume','Adj Close','ischange_bigger_1_tmr','day_1_change_tmr'], 1)
        newdata = newdata.ix[-1].dropna().tolist()
        newdata = np.array(newdata).reshape(1,-1)
        try:
            signal = machine.predict(newdata)
        except:
            pass
        if signal == 1:
            print 'find signal in %s' % file
            try:
                score = machine.predict_proba(newdata)
            except:
                pass
            observes[file[0:6]]=score[-1]
    
    suggest = pd.DataFrame(observes).transpose()
    
    #save file
    outfolder =  workfolder+'stocksuggest/' + date.today().strftime("%Y%m%d")+ '/'
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outfile = outfolder + anlysisfilename + '.csv'
    
    suggest.to_csv(outfile)
    
    return
    
if __name__ == '__main__':
    
    #SVMfromfile() 
    #suggestbySVC()
    Treefromfile()
    
    suggestbyTree()
    suggestbyTree(anlysisfilename='Tree2.p')
    #MLPfromfile()
    