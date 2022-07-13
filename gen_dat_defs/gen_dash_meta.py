# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 16:49:50 2020

@author: muril
"""
#---------------------#
#--- gen_dash_meta ---#
#---------------------#
#--- Goal: 
#---    Generate meta files for each run_id within the dashboard_db.csv
#--- Dependencies:
#---        1. The dashboard must have a column with the base meta that will be used as template
#---        2. The dashboard must also have all of the following keys: lat, lon, plan_year...

def df_csv(f:str):
    
    #--------------------------------------------#
    #--- Reads CSV file as a Pandas DataFrame ---#
    #--------------------------------------------#
    #   f   : Input filename (.CSV)
    #--------------------------------------------#
    
    from pandas import DataFrame, read_csv
    
    #--- Open csv as DataFrame
    try:
        df    = DataFrame(read_csv(f))        
    except UnicodeDecodeError:
        df    = DataFrame(read_csv(f, encoding='latin-1'))
        
    return(df)


def gen_dash_meta(dash,
                  wd_o    = '/sim_db'):
    
    #--- List of driving data
    #dash_nm = 'dashboard_db.csv'
    #wd_o    = '/results'
    
    #--- load libs
    import datetime  as dt
    import os
    #from df_csv import df_csv
        
    #--- filter by gen_meta and run_jules
    dash = dash[:][dash['gen_meta']]
    dash = dash[:][dash['run_jules']]
    
    for run_id in dash['run_id']:
        
        print('Generating meta file for run_id: '+ str(run_id))
        
        f = dash['run_id'] == run_id
        
        #--- open template
        temp_nm = dash['meta_base_temp'][f].values[0]
        temp_df = df_csv('templates/'+temp_nm)
            
        #--- get data
        lat     = dash['lat'][f].values[0]
        lon     = dash['lon'][f].values[0]
        p_yr    = dash['plan_year'][f].values[0]
        h_yr    = dash['harv_year'][f].values[0]
        p_doy   = dash['plan_doy'][f].values[0]
        h_doy   = dash['harv_doy'][f].values[0]
        spinup  = dash['spinup_days'][f].values[0]    
        fl_irr  = dash['full_irrigation'][f].values[0]    
            
        #--- Compute dates    
        p_date = dt.datetime(p_yr,1,1) + dt.timedelta(days = (int(p_doy)-1))
        h_date = dt.datetime(h_yr,1,1) + dt.timedelta(days = (int(h_doy)-1))
        s_date = p_date - dt.timedelta(days = int(spinup))
        e_date = h_date + dt.timedelta(days = 1)    
        
        #--- mon output must start at first day of each month
        o_date = dt.datetime(s_date.year, s_date.month, 1)
        
        if o_date < s_date:
           if o_date.month == 12:
               o_date = dt.datetime(s_date.year+1, 1, 1)
           else:
               o_date = dt.datetime(s_date.year,s_date.month+1, 1)
               
        #-------------------#
        #--- write dates ---#
        #-------------------#
        
        temp_df.loc[temp_df['variable'] == 'main_run_start','val'] = s_date.strftime("'%Y-%m-%d %H:%M:%S'")
        temp_df.loc[temp_df['variable'] == 'main_run_end','val']   = e_date.strftime("'%Y-%m-%d %H:%M:%S'")
        temp_df.loc[temp_df['variable'] == 'output_start','val']   = o_date.strftime("'%Y-%m-%d %H:%M:%S'")
        
        #--- DOYs
        sow_arr = temp_df['array_id'][temp_df['val'] == "'cropsowdate'"].values[0]
        har_arr = temp_df['array_id'][temp_df['val'] == "'croplatestharvdate'"].values[0]
        
        temp_df.loc[(temp_df['variable'] == 'const_val') & (temp_df['array_id'] == sow_arr),'val'] = p_doy
        temp_df.loc[(temp_df['variable'] == 'const_val') & (temp_df['array_id'] == har_arr),'val'] = h_doy
        
        #--- lat/lon
        temp_df.loc[temp_df['variable'] == 'latitude','val']  = lat
        temp_df.loc[temp_df['variable'] == 'longitude','val'] = lon
        
        #--- Irrigated?
        if fl_irr:
            #--- Full Irrigation
            temp_df.loc[temp_df['variable'] == 'const_frac_irr','val'] = 1
        else:
            #--- Rainfed or irrigation was added to precip
            temp_df.loc[temp_df['variable'] == 'const_frac_irr','val'] = 0
          
        #--- run_id
        for i in temp_df.index:
            if '<run_id>' in str(temp_df.loc[i,'val']): 
                temp_df.loc[i,'val'] = temp_df.loc[i,'val'].replace('<run_id>',str(run_id))
                
        #--- write results
        temp_df.to_csv(os.getcwd()+wd_o+'/meta_'+run_id+'.csv',
                       index = False)
                
    