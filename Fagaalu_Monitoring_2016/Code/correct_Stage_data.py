# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 22:47:10 2016

@author: atm19
"""
#
correction_list = [['2/6/2016 16:15','2/7/2016 16:00','10'],['2/17/2016 16:15','2/27/2016 16:00','10']]

corrections = pd.DataFrame(correction_list,columns=['T1_datetime','T2_datetime','zshift_cm'])


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
    #PTdata['stage_cm']=PTdata['corrected_stage_cm'].where(PTdata['corrected_stage_cm']>0,PTdata['stage_cm'])#.round(0)
    return raw_stage
    
raw_stage = pd.DataFrame.from_csv(maindir+'3-LBJ/LBJ-PT-Stage-raw.csv')

stage = correct_Stage_data(corrections,raw_stage)#.to_csv((maindir+'3-LBJ/LBJ-PT-Stage-corrected.csv')