# -*- coding: utf-8 -*-
"""
#--------------------------------------#
#--- Read netCDF outputs from JULES ---#
#--------------------------------------#

#---> Created on Feb-2020

#---> Required Packages:
#---> netCDF4 (pip install netCDF4)
#---> Source: https://unidata.github.io/netcdf4-python/netCDF4/index.html

#---> Plots: https://python-graph-gallery.com/

#---> @author: Murilo Vianna
"""

def read_ncdf(nc_nm:str,
              save_out = True):
    
    #--------------------------------------------------------------#
    #---------------------- update_nml_setup ----------------------# 
    #--------------------------------------------------------------#
    #--- Goal: 
    #---    Reads netCDF output files from JULES and converts to dataframe
    #--- Parameters: 
    #---    nc_nm           : netCDF filename for reading    
    #---    save_out        : Logical flag to save dataframes as CSV [optional]
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    from netCDF4 import Dataset
    import pandas as pd
    import numpy  as np
    
    #--- open ncdf
    jules_nc = Dataset(nc_nm, "r", format="NETCDF4")
    
    #--- List of variables within nc
    var_l_nc = list(jules_nc.variables.keys())
    
    #--- Variables with same dimension
    l_v_dim = []
    l_v_uni = []
    for v in var_l_nc:
        l_v_dim.append(jules_nc[v].dimensions)
        l_v_uni.append(jules_nc[v].units)
        
    df_dims = pd.DataFrame({'variable'   : var_l_nc,
                            'dimensions' : l_v_dim ,
                            'units'      : l_v_uni})
    
    #--- Sort by dimensions
    df_dims = df_dims.sort_values(by=['dimensions'])
    
    #--- Unique dimensions
    uni_dims = df_dims['dimensions'].drop_duplicates().reset_index(drop=True)
        
    dic_out = {}
    for uni_d in uni_dims:
        
        var_l = df_dims['variable'][df_dims['dimensions'] == uni_d]
    
        #--- Get variables list into this dimension
        init_df = True
        for v in var_l:
        
            if not v in var_l_nc:
                import sys
                msg = "Error: Variable '"+v+"' not found on netCDF file '"+nc_nm+"'\nThe variables of this file are:"+str(var_l_nc)
                print(msg+'\nFile not Read.')
                sys.exit(1)
            
            #--- Get variable infos
            v_nmdim = jules_nc[v].dimensions
            v_shape = jules_nc[v][:].shape
           
            #--- Index netcdf variables by dimension size
            if init_df:
                
                init_df = False
                init_d  = True
                
                for d in v_nmdim:
                                    
                    d_rep = np.arange(1,np.array(v_shape)[np.array(v_nmdim) == d][0]+1)                
                    
                    if init_d:
                        d_vec = np.repeat(d_rep, repeats = np.prod(np.array(v_shape)[np.array(v_nmdim) != d]))
                        df_v  = pd.DataFrame({d : d_vec})
                        init_d = False
                        
                    else:                    
                        d_vec = list(d_rep) * np.prod(np.array(v_shape)[np.array(v_nmdim) != d])
                        df_v   = df_v.join(pd.DataFrame({d : d_vec}))
            
            #--- Bind with variable data
            if v in df_v.columns:
                df_v = df_v.join(pd.DataFrame({(v+'_value') : jules_nc[v][:].ravel().data}))
            else:
                df_v = df_v.join(pd.DataFrame({v : jules_nc[v][:].ravel().data}))
        
        #--- Append results
        out_nm = nc_nm.split('/')[-1].replace('.nc','')
        out_nm = out_nm.split('\\')[-1].replace('.nc','')
        out_nm = out_nm+"."+"_".join(list(v_nmdim))
        dic_out[out_nm] = df_v
        
        if save_out:
            #--- Export to CSV
            out_fn  = nc_nm.replace('.nc','')
            out_fn  = out_fn+"."+"_".join(list(v_nmdim))+'.csv'
            df_v.to_csv(out_fn, index = None, header=True)
    
    #--- Overall dimensions info
    dic_out[out_nm+'.info'] = df_dims
    
    if save_out:
        #--- Export dimensions file
        out_fn  = nc_nm.replace('.nc','')
        df_dims.to_csv(out_fn+'.info.csv', index = None, header=True)
        
    #--- Close netCDF
    jules_nc.close()
    
    #--- Return results
    return(dic_out)
