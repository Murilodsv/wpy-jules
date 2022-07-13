# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:55:34 2020

@author: muril
"""

def read_obs(run_id :str,
             wd     :str):
    
    #--- Load Global Packages
    import util         as u
    
    #--- sub ids
    sub_id = run_id[0:2]
    
    #------------------------------------------------------------------------#
    #------------------------------------------------------------------------#
    def filter_ID(df,
                  fn:str,
                  fv):
        #----------------------------------------#
        #--- Local def for filtering df by ID ---#
        #----------------------------------------#
        
        if not fn in df.keys():
            print('\nWarning: There is no column called '+fn+' in dataframe provided')
        else:
            
            if type(fv) == str or type(fv) == float or type(fv) == int:
                #--- Unique values
                len_df = len(df[:][df[fn]==fv])
                if len_df == 0:
                    df = None
                else:
                    return(df[:][df[fn]==fv])
                
            else:
                #--- list/array/etc
                len_df = len(df[:][df[fn].isin(fv)])
                if len_df == 0:
                    df = None
                else:
                    return(df[:][df[fn].isin(fv)])
                
    #------------------------------------------------------------------------#
    #------------------------------------------------------------------------#
    
    #-----------------#
    #--- Read Data ---#
    #-----------------#
    
    #--- Read atmospheric data
    try:
        atmo    = u.df_csv(wd+'/obs_db/atmo/'+sub_id+"_atmo_data.csv")
        atmo    = filter_ID(atmo, 'run_id', run_id)        
        if type(atmo) == type(None): print('\nWarning: No atmospheric observations to compare for ID: '+run_id)        
    except FileNotFoundError:
        print('\nWarning: No file for atmospheric observations to compare for ID: '+run_id)
        atmo = None
    
    #--- Read soil data
    try:
        soil    = u.df_csv(wd+'/obs_db/soil/'+sub_id+"_soil_data.csv")
        soil    = filter_ID(soil, 'run_id', run_id)        
        if type(soil) == type(None): print('\nWarning: No soil observations to compare for ID: '+run_id)
    except FileNotFoundError:
        print('\nWarning: No file for soil observations to compare for ID: '+run_id)
        soil = None
    
    #--- Read soil data
    try:
        plan    = u.df_csv(wd+'/obs_db/plan/'+sub_id+"_plan_data.csv")
        plan    = filter_ID(plan, 'run_id', run_id)        
        if type(plan) == type(None): print('\nWarning: No plant observations to compare for ID: '+run_id)
    except FileNotFoundError:
        print('\nWarning: No file for plant observations to compare for ID: '+run_id)
        plan = None
    
    #--- Return observed data
    return({'atmo' : atmo,
            'soil' : soil,
            'plan' : plan})        

