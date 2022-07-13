# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:54:26 2020

@author: muril
"""

def read_JULES_out(base_nml,
                   run_id   :str,
                   res_CSV  :bool,                   
                   wd_run   :str,
                   time_idx = True,
                   clean_res= True):
    
    #-------------------------------------------------------#
    #----------------- read_JULES_out ----------------------# 
    #-------------------------------------------------------#
    #--- Goal: 
    #---    Read JULES outputs as dataframes
    #--- Parameters: 
    #---    base_nml    : DataFrame containing all info setup of namelists (e.g. output of update_nml_setup())
    #---    run_id      : Running ID
    #---    res_CSV     : Boolean flag to save results as CSV
    #---    wd_run      : Running Directory
    #---    time_idx    : Calculate time indexers? (e.g. DOY/DAS/DAP/YEAR/DATE...)
    #---    clean_res   : Drop the pft and cpft dimensions that are not for the run_id
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #-------------------------------------------------------#
    
    import get_netcdf   as rncdf
    from time import time
    
    #--- Track progress
    start_time = time()
    
    print('\n!-----------------------!'+
          '\n!--- Reading Results ---!'+
          '\n!-----------------------!\n')
    
    #--- Get output names
    l_prof = base_nml['val'][(base_nml['namelist'] == 'jules_output_profile') & 
                              (base_nml['variable'] == 'profile_name')].str.replace("'","").values
                             
    #--- Read for all profiles
    res_run_id = {}
    for prof_nm in l_prof:
                
        #--- Output filename
        out_nc_fn = run_id+'.'+prof_nm+'.nc'
        
        #--- Read output netCDF and append to a dictonary
        res_run_id = {**res_run_id, **rncdf.read_ncdf(wd_run+'/namelists/output/'+out_nc_fn, res_CSV)}
    
    if time_idx:
        #-----------------------------#
        #--- Compute time indexers ---#
        #-----------------------------#
        
        from gen_nml_defs import time_indexer        
        res_run_id = time_indexer(res_run_id, base_nml, u = 's')
        
        #--- Update CSV files
        if res_CSV:
            for k in res_run_id.keys():
                res_run_id[k].to_csv(wd_run+'/namelists/output/'+k+'.csv', index = None, header=True)
                
    if clean_res:
        #---------------------#
        #--- Clean Results ---#
        #---------------------#
        
        import py_jules_constants as c
        
        #--- Crop name from run_id code
        crop_nm = c.crop_codes['crop'][c.crop_codes['crop_code'] == run_id[0:2]].values[0]
        
        if crop_nm == 'Sugarcane' or crop_nm == 'Sorghum':
            # *** Patch for Sugarcane and Sorghum:
            # *** Both will be run as the Maize tile
            crop_nm_tl = 'Maize'
        else:
            crop_nm_tl = crop_nm
        
        #--- Get only the corresponding cpft and pft results
        pft_id      = c.id_crop_pft['n_id'][c.id_crop_pft['crop'] == crop_nm_tl].values[0]
        cpft_id     = c.id_crop_par['n_id'][c.id_crop_par['crop'] == crop_nm_tl].values[0]
        
        #--- Drop unecessary 
        for k in res_run_id.keys():
            if 'pft'  in res_run_id[k].keys(): res_run_id[k] = res_run_id[k][:][res_run_id[k]['pft']  == pft_id]
            if 'tile' in res_run_id[k].keys(): res_run_id[k] = res_run_id[k][:][res_run_id[k]['tile'] == pft_id]
            if 'cpft' in res_run_id[k].keys(): res_run_id[k] = res_run_id[k][:][res_run_id[k]['cpft'] == cpft_id]            
    
    #--- track time
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))
    
    #--- Return
    return(res_run_id)
