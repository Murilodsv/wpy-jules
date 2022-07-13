# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 13:03:08 2020

@author: muril
"""

def get_res(l_res,
            res,
            time_idx  = ['year','doy','dap','das','date'],
            dim_idx   = ['time','soil','pft','cpft']):
    
    #----------------------------------------------------------#
    #------------------------- get_res ------------------------# 
    #----------------------------------------------------------#
    #--- Goal: 
    #---    Get a list of outputs from JULES outputs converted to DataFrame
    #--- Parameters: 
    #---    l_res       : List of simulations outputs to be extracted
    #---    res         : Dictionary with the collection of outputs from JULES netCDF (e.g. outputs of py_jules_run())
    #---    time_idx    : Time indexers to be added to outputs
    #---    dim_idx     : Dimension indexers to be added to outputs
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------# 
    
    #--- Find variables in simulation results
    ini_res = True
    for v in l_res:
        
        lookup_res = True
        for k_r in res.keys():
            if not '.info' in k_r:                        
                if v in res[k_r].keys():
                                                                             
                    #--- found results ---#
                    if lookup_res:
                        
                        print('Variable '+v+' found in simulation output '+k_r)
                        
                        #--- columns to get                        
                        col_get = time_idx
                        for d in dim_idx:                            
                            if d in res[k_r].keys(): col_get = col_get + [d]
                        col_get = col_get + [v]
                        
                        #--- get df                        
                        df_res_k = res[k_r][col_get]
                        df_res_k = df_res_k.rename(columns = {v:'sim_value'})
                        df_res_k['sim_code'] = v
                        
                        #--- Stop looking up
                        lookup_res = False
                        
                        if ini_res:
                            df_res  = df_res_k
                            ini_res = False
                        else:
                            df_res = df_res.append(df_res_k,sort=False)
                    else:
                        print('Warning: Variable '+v+' also found in simulation output '+k_r+', but only the first match will be used.\nPlease check meta information or output profile setup.')
                            
        if lookup_res:
            print('Warning: Variable '+v+' not found in any simulation outputs.\nPlease check meta information or output profile setup.')
    
    #--- Make sure all dimension idx are in output
    for d in dim_idx:
        if not d in df_res.keys(): df_res[d] = 'NaN'
    
    #--- Reorder cols so that all outputs are similar
    reorder_col = time_idx + dim_idx + ['sim_code','sim_value']    
    
    return(df_res[reorder_col])
    