# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:39:11 2020

@author: muril
"""

def time_indexer(res,
                 base_nml,
                 u = 's'):
    
    #-------------------------------------------------------#
    #------------------- time_indexer ----------------------# 
    #-------------------------------------------------------#
    #--- Goal: 
    #---    Compute time indexers for JULES outputs (e.g. dates/doy/year/...)
    #--- Parameters: 
    #---    res         : A dictionary containing JULES results as dataframe (e.g. outputs from read_JULES_out())
    #---    base_nml    : DataFrame containing all info setup of namelists (e.g. output of update_nml_setup())
    #---    u           : Time Units of JULES simulations (default is seconds)
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #-------------------------------------------------------#
    
    import pandas as pd
    from datetime import datetime
    import datetime as dt
    
    #--------------------------------- local def -----------------------------#
    def get_var_array_id(var_nm:str,
                         var_nm_idx:str,
                         nml,
                         base_nml):
        #------------ get_var_array_id --------------#
        #--- Goal:
        #---    To get a variable form namelist base from it's array_id
        #--- Parameters:
        #---    var_nm      : Variable name for JULES
        #---    var_nm_idx  : Variable name as declared in namelist
        #---    nml         : Namelist name
        #---    base_nml    : Base namelist file CSV
        #--------------------------------------------#        
    #--------------------------------- local def -----------------------------#
        try:
            #--- get array id
            array_id = base_nml['array_id'][(base_nml['namelist'] == nml) & 
                               (base_nml['val'] == var_nm)].values[0]
            #--- get variable
            val      = base_nml['val'][(base_nml['namelist'] == nml) & 
                               (base_nml['variable'] == var_nm_idx)  & 
                               (base_nml['array_id'] == array_id)].values[0]
            
            return(val)
        except:
            return(None)
    
    #--- Get time info from base namelist    
    run_ini = base_nml['val'][(base_nml['namelist'] == 'jules_time') & (base_nml['variable'] == 'main_run_start')].values[0].replace("'","")
    run_end = base_nml['val'][(base_nml['namelist'] == 'jules_time') & (base_nml['variable'] == 'main_run_end')].values[0].replace("'","")
    
    #--- get sow date    
    sow_doy = get_var_array_id("'cropsowdate'","const_val","jules_crop_props",base_nml)
    
    if type(sow_doy) == type(None):
        print('Warning: Sow-date not found in namelists. Value will be set to 1.')
        sow_doy = 1
    else:
        sow_doy = int(float(sow_doy))
    
    #--- get harvest date
    har_doy = get_var_array_id("'croplatestharvdate'","const_val","jules_crop_props",base_nml)
    
    if type(har_doy) == type(None):
        print('Warning: Harvest date not found in namelists. Value will be set to 1.')
        har_doy = 1
    else:
        har_doy = int(float(har_doy))
    
    #--- Convert to datetime object
    run_ini = datetime.strptime(run_ini, '%Y-%m-%d %H:%M:%S')
    run_end = datetime.strptime(run_end, '%Y-%m-%d %H:%M:%S')
    
    #--- list of keys
    l_key = list(res.keys())
    
    #--- Convert to df
    k_df = pd.DataFrame(l_key, columns=['res_keys'])    
    k_df[['run_id','out_prof','variables','info']] = k_df['res_keys'].str.split(".", expand=True)
    
    #--- get out profiles
    l_out_prof = k_df.out_prof.unique()
    
    for op in l_out_prof:
        
        #--- get output profile info
        k_df_lp = k_df[:][k_df['out_prof'] == op]
        
        #--- read time dimension
        try:
            time_dim = res[k_df_lp.res_keys[k_df_lp.variables == 'time'].values[0]]
        except:            
            print('Output profile "'+op+'" of ID '+k_df_lp.run_id.values[0]+' has no time dimension.')
            continue
            
        #--- Broadcast time dimension to all variables within this dimension
        l_key_op = k_df_lp['res_keys'][k_df_lp['variables'] != 'time']
        
        for key_op in l_key_op:
            if 'time' in key_op:
                res_df_op = res[key_op]
                
                #--- merge time dimension
                res_df_op = pd.merge(res_df_op, time_dim, on = 'time')
                
                res_df_op['run_ini']    = run_ini
                res_df_op['run_end']    = run_end
                res_df_op['time_delta'] = pd.to_timedelta(res_df_op['time_value'], unit = 's')
                res_df_op['date']       = res_df_op['run_ini'] + res_df_op['time_delta']
                res_df_op['year']       = res_df_op['date'].dt.year
                
                #-----------#
                #--- DOY ---#
                #-----------#
                d1 = pd.to_datetime(pd.DataFrame({'year'  : res_df_op['year'],
                                                  'month' : [1]*len(res_df_op['year']),
                                                  'day'   : [1]*len(res_df_op['year'])}))
                
                res_df_op['doy_f']  = res_df_op['date'] - d1
                res_df_op['doy_f']  = pd.to_numeric(res_df_op['doy_f']) / 1e9 / 86400 # convert nano-seconds to days                
                res_df_op['doy']    = res_df_op['doy_f'].astype(int) + 1
                
                #-----------#
                #--- DAP ---#
                #-----------#
                
                sow_date = datetime.strptime('01/01/'+str(run_ini.year), "%d/%m/%Y") + dt.timedelta(sow_doy) 
                
                if sow_date > run_end:
                    #--- there were probably a spin-off run prior to sow and sowing date was close to the end of year
                    sow_date = datetime.strptime('01/01/'+str(run_ini.year-1), "%d/%m/%Y") + dt.timedelta(sow_doy) 
                
                if (run_end - sow_date).days > 366:
                    #--- there were probably a spin-off at the begining of year so the sowing date was thrown back 1 year
                    sow_date = datetime.strptime('01/01/'+str(run_ini.year+1), "%d/%m/%Y") + dt.timedelta(sow_doy) 
                
                res_df_op['dap_f']  = pd.to_numeric(res_df_op['date'] - sow_date) / 1e9 / 86400 # convert nano-seconds to days                
                res_df_op['dap']    = res_df_op['dap_f'].astype(int) + 1
                
                #-----------#
                #--- DAS ---#
                #-----------#
                
                res_df_op['das_f']  = res_df_op['date'] - run_ini
                res_df_op['das_f']  = pd.to_numeric(res_df_op['das_f']) / 1e9 / 86400 # convert nano-seconds to days                
                res_df_op['das']    = res_df_op['das_f'].astype(int)
                
                #--- Update res
                res[key_op] = res_df_op
                
    #--- Return updated res
    return(res)
                