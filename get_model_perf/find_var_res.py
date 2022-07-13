# -*- coding: utf-8 -*-
"""
Created on Wed May  6 09:53:32 2020

@author: muril
"""

def find_var_res(v,
                 res,
                 time_idx):
    
    #----------------------------------------------------------#
    #---------------------- find_var_res ----------------------# 
    #----------------------------------------------------------#
    #--- Goal: 
    #---    Find output variable in JULES results dictionary
    #--- Parameters: 
    #---    v           : Variable name
    #---    res         : Results dictionary (see py_jules_run())    
    #---    time_idx    : Time indexers to be imported from res dic
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    #--- initialize lookup
    lookup_res = True
    for k_r in res.keys():
        if not '.info' in k_r:                        
            if v in res[k_r].keys():
                                                                         
                #--- found ya!
                if lookup_res:
                    
                    print('Variable '+v+' found in simulation output '+k_r)
                    df_res_k = res[k_r][time_idx + [v]]
                    df_res_k = df_res_k.rename(columns = {v:'sim_value'})
                    df_res_k['sim_code'] = v
                    
                    #--- Stop looking up
                    lookup_res = False                    
                    
                else:
                    print('Warning: Variable '+v+' also found in simulation output '+k_r+', but only the first match will be used.\nPlease check meta information or output profile setup.')
                        
    if lookup_res:
        print('Warning: Variable '+v+' not found in simulation outputs.')
        df_res_k = None
    
    return(df_res_k)