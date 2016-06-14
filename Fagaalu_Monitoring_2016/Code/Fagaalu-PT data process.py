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
import matplotlib
import matplotlib.pyplot as plt
## Set Pandas display options
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.width', 180)
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 10)
#pd.set_option('display.precision', 3)


#plt.close('all')

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

#%%

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
LBJ_PT_raw_data['Abs Pres, kPa'] = LBJ_PT_raw_data['Abs Pres, kPa']*0.0980665
## BAROMETRIC COMPENSATION
LBJ_PT_raw_data['Baropress'] = LBJ_Barologger_raw_data['Abs Pres, kPa']
LBJ_PT_raw_data['Pressure_compensated'] = LBJ_PT_raw_data['Abs Pres, kPa']-LBJ_PT_raw_data['Baropress']
LBJ_PT_raw_data['raw_stage_cm'] = LBJ_PT_raw_data['Pressure_compensated']*0.102*100.0
LBJ_PT_raw_data = LBJ_PT_raw_data.reindex(pd.date_range(start2016,stop2016,freq='5Min'))

LBJ_PT_raw_data['raw_stage_cm'] = LBJ_PT_raw_data['raw_stage_cm'].round(1)


## Save for later
LBJ_PT_raw_data.to_csv(maindir+'3-LBJ/LBJ-PT-Stage-raw.csv')



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
FOREST_PT_raw_data['raw_stage_cm'] = FOREST_PT_raw_data['Pressure_compensated']*0.102*100.0
FOREST_PT_raw_data = FOREST_PT_raw_data.reindex(pd.date_range(start2016,stop2016,freq='5Min'))

FOREST_PT_raw_data['raw_stage_cm'] = FOREST_PT_raw_data['raw_stage_cm'].round(1)
## Save for later
FOREST_PT_raw_data.to_csv(maindir+'1-FOREST/FOREST-PT-Stage-raw.csv')



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
QUARRY_RG_1Min['Events_1Min'] = QUARRY_RG_1Min['Events_Cum_1Min'] - QUARRY_RG_1Min['Events_Cum_1Min'].shift(1).fillna(0) ## fillna(0) is for the very first value, it would be NaN when shifted down
QUARRY_RG_1Min['Events_15Min'] = QUARRY_RG_1Min['Events_Cum_15Min'].dropna() - QUARRY_RG_1Min['Events_Cum_15Min'].dropna().shift(1).fillna(0) ## fillna(0) is for the very first value, it would be NaN when shifted down
## Events to mm
QUARRY_RG_1Min['mm_1Min'] = QUARRY_RG_1Min['Events_1Min']*0.254 ##hundredths to mm
QUARRY_RG_1Min['mm_15Min'] = QUARRY_RG_1Min['Events_15Min']*0.254 ##hundredths to mm
## Reindex into a 15Min interval
QUARRY_RG = QUARRY_RG_1Min[['mm_15Min']].reindex(pd.date_range(start2016,stop2016,freq='15Min'))

## save for later
QUARRY_RG.to_csv(maindir+'2-QUARRY/QUARRY-Precip_15Min-'+now_date+'.csv')

#%%

### PLOTTING RAW DATA

fig, (precip, pressure, stage, turb) = plt.subplots(4,1,figsize=(14,8),sharex=True) 
fig.suptitle('Raw data input')
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
stage.plot_date(LBJ_PT_raw_data['raw_stage_cm'].index, LBJ_PT_raw_data['raw_stage_cm'], ls='-', marker='None', label='LBJ-PT',color='r')
## FOREST-PT
stage.plot_date(FOREST_PT_raw_data['raw_stage_cm'].index, FOREST_PT_raw_data['raw_stage_cm'], ls='-', marker='None', label='FOREST-PT',color='g')
## fmt
stage.legend(loc='upper left')
stage.set_ylabel('cm')
stage.set_xlim(start2016,stop2016)

#import matplotlib.dates as mdates
stage.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
plt.show()

#%%

#### STAGE CORRECTION

## Drop bad values (from instrument readout, bad data etc)


def drop_data(pt_data,t1,t2=''):
    #print pt_data.dropna()
    ## set times
    if t2=='':
        t2 = t1
    drop_dates = pd.date_range(t1,t2,freq='5Min')
    cleaned = pt_data = pt_data.drop(pt_data.ix[drop_dates[0:]].index) ## I'm sure there's an easier way but this slices the index off the PT df based on the list of dates to drop 
    reindexed = pt_data.reindex(pd.date_range(start2016,stop2016,freq='5Min'))
    return reindexed



## LBJ
LBJ_PT_raw_data = pd.DataFrame.from_csv(maindir+'3-LBJ/LBJ-PT-Stage-raw.csv')

LBJ_PT_raw_data = drop_data(LBJ_PT_raw_data,'02/05/2016 13:05','02/05/2016 13:15')
LBJ_PT_raw_data = drop_data(LBJ_PT_raw_data,'02/18/2016 10:10','02/18/2016 10:25')
LBJ_PT_raw_data = drop_data(LBJ_PT_raw_data,'03/02/2016 10:25','03/02/2016 10:30') ## this deletes 2 rows: 10:25 and 10:30
LBJ_PT_raw_data = drop_data(LBJ_PT_raw_data,'04/12/2016 10:20','04/12/2016 10:35') 
LBJ_PT_raw_data = drop_data(LBJ_PT_raw_data,'05/04/2016 11:45','05/04/2016 12:05')


## FOREST
FOREST_PT_raw_data = pd.DataFrame.from_csv(maindir+'1-FOREST/FOREST-PT-Stage-raw.csv')

FOREST_PT_raw_data = drop_data(FOREST_PT_raw_data,'03/02/2016 09:10')
FOREST_PT_raw_data = drop_data(FOREST_PT_raw_data,'04/12/2016 09:10','04/12/2016 09:15')
FOREST_PT_raw_data = drop_data(FOREST_PT_raw_data,'05/04/2016 10:10','05/04/2016 10:30')



#%%

### PLOTTING CORRECTED STAGE DATA

fig, (precip, pressure, stage, turb) = plt.subplots(4,1,figsize=(14,8),sharex=True) 
fig.suptitle('Data dropout corrected')
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
stage.plot_date(LBJ_PT_raw_data['raw_stage_cm'].index, LBJ_PT_raw_data['raw_stage_cm'], ls='-', marker='None', label='LBJ-PT',color='r')
## FOREST-PT
stage.plot_date(FOREST_PT_raw_data['raw_stage_cm'].index, FOREST_PT_raw_data['raw_stage_cm'], ls='-', marker='None', label='FOREST-PT',color='g')
## fmt
stage.legend(loc='upper left')
stage.set_ylabel('cm')
stage.set_xlim(start2016,stop2016)

#import matplotlib.dates as mdates
stage.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
plt.show()

#%%


## Correct Base Level shifts

def correct_Stage_data(corrections,raw_stage):
    print 'Correcting stage...'
    Correction=pd.DataFrame()
    for correction in corrections.iterrows():
        #print correction[1]
        t1 = pd.to_datetime(correction[1]['T1_datetime'])
        t2 = pd.to_datetime(correction[1]['T2_datetime'])
        z = correction[1]['zshift_cm']    
        print t1,t2, z
        ## Make time series of zshift correction factors
        Correction = Correction.append(pd.DataFrame({'zshift_cm':float(z)},index=pd.date_range(t1,t2,freq='5Min')))
    ## Make complete time series    
    Correction = Correction.reindex(pd.date_range(start2016,stop2016,freq='5Min'))
    ## Add correction factors to PT data
    raw_stage['zshift_cm'] = Correction['zshift_cm']
    ## Calculate corrected stage
    raw_stage['corrected_stage_cm'] = raw_stage['raw_stage_cm'] + raw_stage['zshift_cm']
    ## Add in the part of the timeseries that did not need correction
    raw_stage['stage_cm']=raw_stage['corrected_stage_cm'].where(raw_stage['corrected_stage_cm']>0,raw_stage['raw_stage_cm'])#.round(0)
    return raw_stage


## IF YOU NEED ALREADY MADE DATA  
#LBJ_PT_raw_data= pd.DataFrame.from_csv(maindir+'3-LBJ/LBJ-PT-Stage-raw.csv')

## LBJ Final Stage    
#LBJ_correction_list = [['2/6/2016 16:15','2/7/2016 16:00','10'],['2/17/2016 16:15','2/27/2016 16:00','10']]
LBJ_correction_list = [[start2016,stop2016,'0']]
LBJ_correction_df = pd.DataFrame(LBJ_correction_list,columns=['T1_datetime','T2_datetime','zshift_cm'])
LBJ_PT_final_data = correct_Stage_data(LBJ_correction_df,LBJ_PT_raw_data)
## Output
LBJ_PT_final_data.to_csv(maindir+'3-LBJ/LBJ-PT-Stage-final.csv')

## FOREST Final Stage
FOREST_correction_list = [[start2016,stop2016,'0']] ## For no corrections
FOREST_correction_df = pd.DataFrame(FOREST_correction_list,columns=['T1_datetime','T2_datetime','zshift_cm'])
FOREST_PT_final_data  = correct_Stage_data(FOREST_correction_df,FOREST_PT_raw_data)
## Output
FOREST_PT_final_data.to_csv(maindir+'1-FOREST/FOREST-PT-Stage-final.csv')

#%%

### PLOTTING CORRECTED/FINAL STAGE DATA

fig, (precip, pressure, stage, turb) = plt.subplots(4,1,figsize=(14,8),sharex=True) 
fig.suptitle('Base level corrected')
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
stage.plot_date(LBJ_PT_raw_data['raw_stage_cm'].index, LBJ_PT_raw_data['raw_stage_cm'], ls='-', marker='None', label='LBJ-PT',color='r')
## FOREST-PT
stage.plot_date(FOREST_PT_raw_data['raw_stage_cm'].index, FOREST_PT_raw_data['raw_stage_cm'], ls='-', marker='None', label='FOREST-PT',color='g')
## fmt
stage.legend(loc='upper left')
stage.set_ylabel('cm')
stage.set_xlim(start2016,stop2016)

#import matplotlib.dates as mdates
stage.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d %H:%M'))
plt.show()

#%%


## This block calcuates Q from Manning's equation for each cm of stage
## if this already exists as a csv, just open the csv and get Q, indexed by stage
## if it doesn't exist, create it; if you need a new one, delete the csv and run it
if 'LBJ_Man' not in locals():
    try:
        ## Import final/corrected stage data from csv's (created in Module 1)
        LBJ_stage = pd.DataFrame.from_csv(maindir+'3-LBJ/LBJ-PT-Stage-final.csv') ## FINAL/CORRECTED STAGE DATA
        ## Straight from csv
        LBJ_Man_reduced = pd.DataFrame.from_csv(maindir+'3-LBJ/LBJ_Man_reduced.csv')
    except:
        ## Import final/corrected stage data from csv's (created in Module 1)
        LBJ_stage = pd.DataFrame.from_csv(maindir+'3-LBJ/LBJ-PT-Stage-final.csv') ## FINAL/CORRECTED STAGE DATA
        del LBJ_stage['zshift_cm']
        ## Calculate discharge from Manning's equation, for each cm of stage
        from Mannings_from_stage import Mannings_Q_from_stage_data
        ## Mannings parameters for the LBJ
        LBJ_S, LBJ_n, LBJ_k = 0.016, .067, 1
        ## Create a dataframe of only the stage values that are recorded
        LBJ_stage_reduced = LBJ_stage['stage_cm'].dropna().round(0).drop_duplicates().order()
        ## Calculate discharge with Mannings on the reduced range of values
        LBJ_Man_reduced = Mannings_Q_from_stage_data(maindir+'3-LBJ/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k, stage_data=LBJ_stage_reduced)
        ## Visualize Stage-Q Rating
        plt.scatter(LBJ_Man_reduced['stage(m)'], LBJ_Man_reduced['Q(m3/s)'])
        ## Save the output to csv
        LBJ_Man_reduced.to_csv(maindir+'3-LBJ/LBJ_Man_reduced.csv')

try:
    del LBJ_stage['zshift_cm']
except:
    pass

## Add to stage
#LBJ_stage['corrected_stage_cm'] = LBJ_stage['corrected_stage_cm'] + 5. ## add 5cm so no zero/negative values???? Not sure what this is from, maybe offset with the AV measurements
LBJ_stage['stage_m'] = LBJ_stage['corrected_stage_cm'].round(0)/100.

## Match discharge to stage records for whole time series
## Add column for Discharge
LBJ_stage['Q(m3/s)'] = np.nan

## Iterate over stage records and add discharge value from the reduced stage record for which Manning's Q was calculated
## This saves you from re-calculating Mannings for each stage value, just do it once for each cm of stage!
for row in LBJ_stage.dropna(how='all').iterrows():
    #print row[0]
    stage = row[1]['stage_m']
    try:
        Q = LBJ_Man_reduced[LBJ_Man_reduced['stage(m)']==stage]['Q(m3/s)'].iloc[0]
        LBJ_stage.loc[row[0],'Q(m3/s)'] = Q
    except:
        print "Can't get Q data from LBJ_Man_reduced"+ str(row[0])+str(stage)
    #print row[0], stage, Q
    # .iloc[row_index,col_index] = value
    # .loc[row_index,col_index] = value
    
## Visualize Q timeseries
fig, Q = plt.subplots(1,1)
Q.plot_date(LBJ_stage.index, LBJ_stage['Q(m3/s)'],marker='None',ls='-',c='r')
## Pass stage data on to discharge df
LBJ_Q = LBJ_stage
## Save the Q timeseries output to csv
LBJ_Q.to_csv(maindir+'3-LBJ/LBJ_Q.csv')

#%%

## FOREST
FOREST_stage = pd.DataFrame.from_csv(maindir+'1-FOREST/FOREST-PT-Stage-final.csv')

### HEC-RAS Model of the DAM structure: Documents/HEC/FagaaluDam.prj
def HEC_piecewise(PTdata):
    if type(PTdata)!=pd.Series:
        PTdata = pd.Series(data=PTdata)
    HEC_a1, HEC_b1 = 9.9132, -5.7184 ## from excel DAM_HEC.xlsx
    HEC_a2, HEC_b2 = 25.823, -171.15 
    HEC_a3, HEC_b3 = 98.546, -3469.4
    
    Func1=PTdata[PTdata<=11]*HEC_a1 + HEC_b1
    Func2=PTdata[(PTdata>11)&(PTdata<=45)]*HEC_a2 + HEC_b2
    Func3=PTdata[PTdata>45]*HEC_a3 + HEC_b3
    AllValues = Func1.append([Func2,Func3])
    return AllValues
    
FOREST_HEC = pd.DataFrame(data=range(0,150),columns=['stage(cm)'])
FOREST_HEC['Q_HEC(L/sec)'] = HEC_piecewise(FOREST_HEC['stage(cm)'])

FOREST_HEC['Q_HEC(L/sec)']= HEC_piecewise(FOREST_HEC['stage(cm)']).values

FOREST_HEC_rating = pd.ols(y=FOREST_HEC['Q_HEC(L/sec)'],x=FOREST_HEC['stage(cm)'],intercept=True) 


#%%



#### Turbidity
#OBSdata_filename = "C:/Users/atm19/Google Drive/AmSamFieldLaptop/Siumu's Folder/1-FOREST/FOREST-OBS/FOREST_Table1.dat"
#
#OBSheaders =pd.DataFrame.from_csv(OBSdata_filename,header=1).columns
#OBSdata = pd.DataFrame.from_csv(OBSdata_filename,header=4,parse_dates=True)
#OBSdata.columns = OBSheaders
#
#OBSdata['index'] = OBSdata.index
#OBSdata = OBSdata.drop_duplicates(cols='index')
#OBSdata = OBSdata.reindex(pd.date_range(start2016,stop2016,freq='15Min'))
#
#OBSdata = OBSdata[OBSdata['Turb_SS']<=4000]
#
#turb.plot_date(OBSdata.index, OBSdata['Turb_SS'], ls='-', marker='None', label='FOREST Turb (SS_Mean)', c='g')
#turb.set_xlim(start2016,stop2016), turb.set_ylim(0,4000)
#turb.set_ylabel('NTU')
#
#
#plt.tight_layout()
#plt.show() 

#import plotly.plotly as py
#from plotly.graph_objs import *
#
#plot_url = py.plot(fig, filename = 'Stage and Turbidity Fagaalu 2015- Jan 2016')
   
        
