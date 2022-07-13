# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 10:36:56 2020

@author: muril
"""

def py_jules_run(run_id,
                 base_nml_fn,
                 driv_id,
                 soil_id,
                 crop_id,
                 crop_nm,
                 wd,
                 wd_sim_db,#debug wd_sim_db = 'sim_db'
                 wd_run,
                 exec_fn,
                 templ_path,
                 verb     = True,
                 res_CSV  = True,
                 time_idx = True,
                 clean_res= True,
                 upd_base_nml= None,
                 copy_sim_db = False,
                 gen_driving = True,
                 del_exe     = True,
                 f_calibrate = False,
                 calib_setup_fn = None):
    
    #-------------------------------------------------------#
    #------------------- py_jules_run ----------------------# 
    #-------------------------------------------------------#
    #--- Goal: 
    #---    Run py-jules simulation
    #--- Parameters: 
    #---    run_id      : Running ID
    #---    wd          : Working Directory
    #---    base_nml_fn : Base namelist filename
    #---    driv_id     : Drive data ID
    #---    soil_id     : Soil data ID
    #---    crop_id     : Crop parameters ID
    #---    crop_nm     : Crop name (e.g. Maize, Rice, Soybean)
    #---    exec_fn     : Name of the JULES executable file (e.g. jules.exe)
    #---    verb        : Verbose flag
    #---    time_idx    : Compute time indexers for outputs (e.g. date,year,doy...)
    #---    clean_res   : Retrieve clean results. if true all cpft and pft dimensions that are for the target crop will be ruled out
    #---    upd_base_nml: Updated base namelist filename
    #---    copy_sim_db : Make a copy of sim_db used into jules_run folder (useful for sensitivity analysis)
    #---    gen_driving : Flag to generate driving data (for sake of time on sensitivity analysis)
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #-------------------------------------------------------#    
    
    import gen_nml_defs as gn
    import shutil
    
    #--- Create Running Environment    
    base_nml = gn.gen_jules_run(run_id,
                                base_nml_fn,
                                driv_id,
                                soil_id,
                                crop_id,
                                crop_nm,
                                wd,
                                wd_sim_db,
                                wd_run,
                                templ_path,
                                verb         = True,
                                upd_base_nml = upd_base_nml,
                                copy_sim_db  = copy_sim_db,
                                gen_driving  = gen_driving,
                                f_calibrate  = f_calibrate,
                                calib_setup_fn = calib_setup_fn)
        
    #--- Copy the executable to the running path (or call rose to compile the code. To be developed...)
    shutil.copy2(wd+'/sim_db/'+exec_fn,
                 wd_run)
    
    #--- Run JULES    
    run_status = gn.run_JULES(exec_fn,wd_run)
    
    #--- Delete exe (for sake of storage)
    if del_exe:
        import os
        os.remove(wd_run+'/'+exec_fn)
            
    #--- Read Outputs (if simulation succeeded)    
    if run_status.returncode == 0:
        res = gn.read_JULES_out(base_nml,
                                run_id,
                                res_CSV,
                                wd_run,
                                time_idx,
                                clean_res)
        
        return(res)
    else:
        return(None)