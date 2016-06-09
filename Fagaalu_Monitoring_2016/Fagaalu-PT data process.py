# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 14:17:48 2015

@author: Alex
"""

## CTRL-SPACE for code completion options

#### Import modules
## Data Processing
import os
import numpy as np
import pandas as pd
#import math
import datetime as dt
import matplotlib.pyplot as plt
## Set Pandas display options
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.width', 180)
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 10)
#pd.set_option('display.precision', 3)


plt.close('all')

#timer
import datetime as dt
now = dt.datetime.now()
print 'Start time: '+now.strftime('%H:%M:%S')
now_date = now.strftime('%d_%m_%Y')


#### DIRECTORIES
Laptop = 'Field'
Laptop = 'Alex'
#Laptop = 'Trent'

if Laptop == 'Field': 
    maindir = "C:/Users/geoguser/Desktop/FieldLaptop/AmSamFieldLaptop/Siumu's Folder/"
    dirs={'main':maindir}
    
if Laptop == 'Alex': 
    maindir = "C:/Users/atm19/Documents/Github/Fagaalu_monitoring/Fagaalu_Monitoring_2016/"
    dirs={'main':maindir}
    
if Laptop == 'Trent': 
    maindir = "C:/Users/atm19/Google Drive/AmSamFieldLaptop/Siumu's Folder/" # <<<< TRENT ADD YOUR PATH HERE
    dirs={'main':maindir}


## Year Interval Times
#start2012, stop2012 = dt.datetime(2012,1,1,0,0), dt.datetime(2012,12,31,11,59)    
#start2013, stop2013 = dt.datetime(2013,1,1,0,0), dt.datetime(2013,12,31,11,59)
#start2014, stop2014 = dt.datetime(2014,1,1,0,0), dt.datetime(2014,12,31,11,59)   
#start2015, stop2015 = dt.datetime(2015,1,1,0,0), dt.datetime(2015,12,31,11,59)   
start2016, stop2016 = dt.datetime(2016,1,1,0,0), dt.datetime(2016,6,1,11,59)   


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


### Barologgers
#my_parser = lambda x: datetime.strptime(x, '%Y%m%d %H%M%s')

## LBJ
Barologger_path = maindir+'3-LBJ/LBJ-Barologger/'
Barologger_raw_data  = pd.DataFrame()
for f in os.listdir(Barologger_path):
    if f.endswith('.csv') == True:
        print f
        raw = Solinst_data_parser(Barologger_path+f)
        raw = raw[['LEVEL','TEMPERATURE']]
        raw.columns  = ['Abs Pres, kPa','Temp, C']
        Barologger_raw_data = Barologger_raw_data.append(raw)
LBJ_Barologger_raw_data= Barologger_raw_data
LBJ_Barologger_raw_data['index'] = LBJ_Barologger_raw_data.index
LBJ_Barologger_raw_data = LBJ_Barologger_raw_data.drop_duplicates(cols='index')
LBJ_Barologger_raw_data = LBJ_Barologger_raw_data.reindex(pd.date_range(start2016,stop2016,freq='5Min'))

## FOREST
Barologger_path = maindir+'1-FOREST/FOREST-Barologger/'
Barologger_raw_data  = pd.DataFrame()
for f in os.listdir(Barologger_path):
    if f.endswith('.csv') == True:
        print f
        raw = Solinst_data_parser(Barologger_path+f)
        raw = raw[['LEVEL','TEMPERATURE']]
        raw.columns  = ['Abs Pres, kPa','Temp, C']
        Barologger_raw_data = Barologger_raw_data.append(raw)
FOREST_Barologger_raw_data = Barologger_raw_data
FOREST_Barologger_raw_data['index']  = FOREST_Barologger_raw_data.index
FOREST_Barologger_raw_data = FOREST_Barologger_raw_data.drop_duplicates(cols='index')
FOREST_Barologger_raw_data = FOREST_Barologger_raw_data.reindex(pd.date_range(start2016,stop2016,freq='5Min'))


        

### LBJ-PT
PT_path = maindir+'3-LBJ/LBJ-PT/'
LBJ_PT_raw_data = pd.DataFrame()
for f in os.listdir(PT_path):
    if f.endswith('cm.csv') == True:
        print f
        raw = Solinst_data_parser(PT_path+f)
        raw = raw[['LEVEL','TEMPERATURE']]
        raw.columns  = ['Abs Pres, kPa','Temp, C']
        LBJ_PT_raw_data = LBJ_PT_raw_data.append(raw)
## CLEAN UP DATA          
LBJ_PT_raw_data = LBJ_PT_raw_data.sort_index()
LBJ_PT_raw_data['index'] = LBJ_PT_raw_data.index
LBJ_PT_raw_data = LBJ_PT_raw_data.drop_duplicates(cols = 'index')
LBJ_PT_raw_data ['Abs Pres, kPa'] = LBJ_PT_raw_data ['Abs Pres, kPa']*0.0980665
## BAROMETRIC COMPENSATION
LBJ_PT_raw_data['Baropress'] = LBJ_Barologger_raw_data['Abs Pres, kPa']
LBJ_PT_raw_data['Pressure_compensated'] = LBJ_PT_raw_data['Abs Pres, kPa']-LBJ_PT_raw_data['Baropress']
LBJ_PT_raw_data['stage cm'] = LBJ_PT_raw_data['Pressure_compensated']*0.102*100.0
LBJ_PT_raw_data = LBJ_PT_raw_data.reindex(pd.date_range(start2016,stop2016,freq='5Min'))

## Save for later
LBJ_PT_raw_data.to_csv(maindir+'3-LBJ/LBJ-PT-Stage-'+now_date+'.csv')



### FOREST-PT
PT_path = maindir+'1-FOREST/FOREST-PT/'
FOREST_PT_raw_data = pd.DataFrame()
for f in os.listdir(PT_path):
    if f.endswith('.csv') == True:
        print f
        raw = Solinst_data_parser(PT_path+f)
        raw = raw[['LEVEL','TEMPERATURE']]
        raw.columns  = ['Abs Pres, kPa','Temp, C']
        FOREST_PT_raw_data = FOREST_PT_raw_data.append(raw)
## CLEAN UP DATA       
FOREST_PT_raw_data = FOREST_PT_raw_data.sort_index()
FOREST_PT_raw_data['index'] = FOREST_PT_raw_data.index
FOREST_PT_raw_data = FOREST_PT_raw_data.drop_duplicates(cols = 'index')
## BAROMETRIC COMPENSATION
FOREST_PT_raw_data['Baropress'] = FOREST_Barologger_raw_data['Abs Pres, kPa']
FOREST_PT_raw_data['Pressure_compensated'] = FOREST_PT_raw_data['Abs Pres, kPa']-FOREST_PT_raw_data['Baropress']
FOREST_PT_raw_data['stage cm'] = FOREST_PT_raw_data['Pressure_compensated']*0.102*100.0
FOREST_PT_raw_data = FOREST_PT_raw_data.reindex(pd.date_range(start2016,stop2016,freq='5Min'))
## Save for later
FOREST_PT_raw_data.to_csv(maindir+'1-FOREST/FOREST-PT-Stage-'+now_date+'.csv')



### Rain Gauge
##my_parser= lambda x: dt.datetime.strptime(x,"%m/%d/%Y %H:%M")
#Timu1 = pd.ExcelFile(maindir+'2-QUARRY/QUARRY-RAIN GAUGE/QUARRY-RAIN GAUGE.xlsx').parse('QUARRY-RAIN_GAUGE-03-02-2016',header=1,index_col=0,parse_cols='B,D',parse_dates=True)#,date_parser=my_parser)
#Timu1['mm'] = Timu1['Events']*0.254 ##hundredths to mm
#Timu1 = Timu1.reindex(pd.date_range(start2015,stop2016,freq='15Min'))
# 
 
##
QUARRY_RG_path = maindir+'2-QUARRY/QUARRY-RAIN GAUGE/'
QUARRY_RG_raw_data = pd.DataFrame()
for f in os.listdir(QUARRY_RG_path):
    if f.endswith('.csv') == True:
        print f
        raw = pd.DataFrame.from_csv(QUARRY_RG_path+f,header=1,parse_dates=1,index_col=1)
        raw = raw.ix[:,1:3]
        raw.columns  = ['Temp, C','Events']
        QUARRY_RG_raw_data = QUARRY_RG_raw_data.append(raw)
## CLEAN UP DATA       
QUARRY_RG_raw_data = QUARRY_RG_raw_data.sort_index()
QUARRY_RG_raw_data['index'] = QUARRY_RG_raw_data.index
QUARRY_RG = QUARRY_RG_raw_data.drop_duplicates(cols = 'index')
## Resample cumulative events to 1 minute (eg. 16:00 to 16:01 has two events at 16:00:15 and 16:00:44 so 16:00=2; next event is at 16:02:13 so 16:01=2 and 16:02=3)
QUARRY_RG_1Min=pd.DataFrame()
QUARRY_RG_1Min['Events_Cum_1Min'] = QUARRY_RG['Events'].resample('1Min',how='last',fill_method='ffill')
QUARRY_RG_1Min['Events_Cum_15Min'] = QUARRY_RG['Events'].resample('15Min',how='last',fill_method='ffill')
## Subtract previous minutes events from the following minute (eg. cumulative events at 16:00=2, and at 16:02=3 so events for 16:02=1) 
QUARRY_RG_1Min['Events_1Min'] = QUARRY_RG_1Min['Events_Cum_1Min'] - QUARRY_RG_1Min['Events_Cum_1Min'] .shift(1).fillna(0) ## fillna(0) is for the very first value, it would be NaN when shifted down
QUARRY_RG_1Min['Events_15Min'] = QUARRY_RG_1Min['Events_Cum_15Min'].dropna() - QUARRY_RG_1Min['Events_Cum_15Min'].dropna().shift(1).fillna(0) ## fillna(0) is for the very first value, it would be NaN when shifted down
## Events to mm
QUARRY_RG_1Min['mm_1Min'] = QUARRY_RG_1Min['Events_1Min']*0.254 ##hundredths to mm
QUARRY_RG_1Min['mm_15Min'] = QUARRY_RG_1Min['Events_15Min']*0.254 ##hundredths to mm
## Reindex into a 15Min interval
QUARRY_RG = QUARRY_RG_1Min[['mm_15Min']].reindex(pd.date_range(start2016,stop2016,freq='15Min'))

## save for later
QUARRY_RG.to_csv(maindir+'2-QUARRY/QUARRY-RAIN GAUGE/Precip_15Min-'+now_date+'.csv')



### PLOTTING RAW DATA

fig, (precip, pressure, stage, turb) = plt.subplots(4,1,figsize=(14,8),sharex=True) 

## PRECIP
precip.plot_date(QUARRY_RG.index, QUARRY_RG['mm_15Min'], color='b',alpha=0.5,ls='steps-pre', marker='None',label='Precip_mm_15Min')
precip.set_ylabel('Precip mm'), precip.set_ylim(0,10)
plt.show() 

### BAROMETRIC and TRANSDUCER PRESSURE

## BAROMETERS
## LBJ-BL-Barologger at LBJ
pressure.plot_date(LBJ_Barologger_raw_data.index, LBJ_Barologger_raw_data['Abs Pres, kPa'],alpha=0.5, ls='-', marker='None', label='LBJ Barologger pressure', color='r')
## FOREST-BL-Barologger at FOREST
pressure.plot_date(FOREST_Barologger_raw_data.index, FOREST_Barologger_raw_data['Abs Pres, kPa'],alpha=0.5, ls='-', marker='None', label='FOREST Barologger pressure', color='g')


## PTs
## LBJ-PT
pressure.plot_date(LBJ_PT_raw_data['Abs Pres, kPa'].index, LBJ_PT_raw_data['Abs Pres, kPa'], ls='-', marker='None', label='LBJ PT pressure',color='r')
## FOREST-PT
pressure.plot_date(FOREST_PT_raw_data['Abs Pres, kPa'].index, FOREST_PT_raw_data['Abs Pres, kPa'], ls='-', marker='None', label='FOREST PT pressure',color='g')
## fmt
pressure.legend(loc='upper left', ncol=2)
pressure.set_ylabel('kPa')
pressure.set_xlim(start2016,stop2016)


### STAGE
## LBJ-PT
stage.plot_date(LBJ_PT_raw_data['stage cm'].index, LBJ_PT_raw_data['stage cm'], ls='-', marker='None', label='LBJ-PT',color='r')
## FOREST-PT
stage.plot_date(FOREST_PT_raw_data['stage cm'].index, FOREST_PT_raw_data['stage cm'], ls='-', marker='None', label='FOREST-PT',color='g')
## fmt
stage.legend(loc='upper left')
stage.set_ylabel('cm')
stage.set_xlim(start2016,stop2016)




### Turbidity
OBSdata_filename = "C:/Users/atm19/Google Drive/AmSamFieldLaptop/Siumu's Folder/1-FOREST/FOREST-OBS/FOREST_Table1.dat"

OBSheaders =pd.DataFrame.from_csv(OBSdata_filename,header=1).columns
OBSdata = pd.DataFrame.from_csv(OBSdata_filename,header=4,parse_dates=True)
OBSdata.columns = OBSheaders

OBSdata['index'] = OBSdata.index
OBSdata = OBSdata.drop_duplicates(cols='index')
OBSdata = OBSdata.reindex(pd.date_range(start2016,stop2016,freq='15Min'))

OBSdata = OBSdata[OBSdata['Turb_SS']<=4000]

turb.plot_date(OBSdata.index, OBSdata['Turb_SS'], ls='-', marker='None', label='FOREST Turb (SS_Mean)', c='g')
turb.set_xlim(start2016,stop2016), turb.set_ylim(0,4000)
turb.set_ylabel('NTU')


plt.tight_layout()
plt.show() 

#import plotly.plotly as py
#from plotly.graph_objs import *
#
#plot_url = py.plot(fig, filename = 'Stage and Turbidity Fagaalu 2015- Jan 2016')
   
        