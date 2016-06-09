# -*- coding: utf-8 -*-
"""
Created on Thu Jun 09 15:55:25 2016

@author: atm19
"""
import pandas as pd
import numpy as np

def Solinst_data_parser(filename):
    
    df = pd.read_csv(filename,names=range(0,5)) ## Read csv
    hdr_row = np.where(df[0]=='Date')[0][0]
    df.columns = df.iloc[hdr_row].values ## find header row and make column names from row values
    df = df[hdr_row+1:]
    df.index = pd.to_datetime(df['Date']+' '+df['Time'])
    ## Make sure data are correct type
    for col in df.columns:
        #print col
        if type(pd.to_datetime(df[col].iloc[0])) == str:
            try:
                #print 'to float'
                df[col] = df[col].astype(np.float)
            except:
                #print 'cant float'
                pass
        elif type(pd.to_datetime(df[col].iloc[0])) == pd.tslib.Timestamp:
            try:
                #print 'to timestamp'
                df[col] = pd.to_datetime(df[col])
            except:
                #print 'cant time'
                pass
    return df
