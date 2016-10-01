# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 18:27:45 2016

@author: LT
"""
import datafetch
from datafetch import yahoofinance_store,dataprepare
import performance
from performance import performace_probability
import stocksuggest
from stocksuggest import bymachine
if __name__ == '__main__':
    
    datafetch.yahoofinance_store.yahoofinance_refresh()
    
    datafetch.dataprepare.addfeature_all()
    datafetch.dataprepare.generate_trainfile()
    performance.performace_probability.add_performance()
    
    stocksuggest.bymachine.Treefromfile()
    
    stocksuggest.bymachine.suggestbyTree()
    stocksuggest.bymachine.suggestbyTree(anlysisfilename='Tree2.p')