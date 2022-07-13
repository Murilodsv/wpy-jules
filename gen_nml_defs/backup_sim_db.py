# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:40:45 2020

@author: muril
"""

def backup_sim_db(run_id,
                  crop_id,
                  driv_id,
                  soil_id,
                  co2_data_fn,
                  wd,
                  wd_run,
                  base_nml_fn,
                  wd_sim_db = 'sim_db'):

    #---------------------------------------------------------------#
    #------------------------ backup_sim_db ------------------------# 
    #---------------------------------------------------------------#
    #--- Goal: 
    #---    Backup sim_db files that can be recycle for sensitivity analysis or parallel runs
    #--- Parameters: 
    #---    run_id      : Running   ID
    #---    crop_id     : Crop      ID
    #---    driv_id     : Drive     ID
    #---    soil_id     : Soil      ID
    #---    co2_data_fn : co2 filename of CSV data in sim_db
    #---    wd          : working dir 
    #---    base_nml_fn : base nml filename .csv
    #---    wd_sim_db   : sim_db sub-folder name
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    import os
    from shutil import copyfile
    
    #--- Erase old data
    try:
        if os.path.exists(wd_run+'/'+wd_sim_db): os.remove(wd_run+'/'+wd_sim_db)
    except:
        import shutil
        shutil.rmtree(wd_run+'/'+wd_sim_db)
    
    os.mkdir(wd_run+'/'+wd_sim_db)
    os.mkdir(wd_run+'/'+wd_sim_db+'/driving')
    os.mkdir(wd_run+'/'+wd_sim_db+'/soil')
    os.mkdir(wd_run+'/'+wd_sim_db+'/crop')
    os.mkdir(wd_run+'/'+wd_sim_db+'/ancillary')
    
    #--- Copy run meta
    copyfile(wd+'/'+wd_sim_db+'/meta_'+run_id+'.csv',
             wd_run+'/'+wd_sim_db+'/meta_'+run_id+'.csv')
    
    #--- Copy base
    copyfile(wd+'/'+wd_sim_db+'/'+base_nml_fn,
             wd_run+'/'+wd_sim_db+'/'+base_nml_fn)
            
    #--- Copy Crop
    copyfile(wd+'/'+wd_sim_db+'/crop/meta_'+crop_id+'.csv',
             wd_run+'/'+wd_sim_db+'/crop/meta_'+crop_id+'.csv')
    
    #--- Copy driving data and meta to running folder
    copyfile(wd+'/'+wd_sim_db+'/driving/data_'+driv_id+'.csv',
             wd_run+'/'+wd_sim_db+'/driving/data_'+driv_id+'.csv')
    
    copyfile(wd+'/'+wd_sim_db+'/driving/meta_'+driv_id+'.csv',
             wd_run+'/'+wd_sim_db+'/driving/meta_'+driv_id+'.csv')
    
    #--- Copy soil data and meta to running folder
    copyfile(wd+'/'+wd_sim_db+'/soil/data_'+soil_id+'.csv',
             wd_run+'/'+wd_sim_db+'/soil/data_'+soil_id+'.csv')
    
    copyfile(wd+'/'+wd_sim_db+'/soil/meta_'+soil_id+'.csv',
             wd_run+'/'+wd_sim_db+'/soil/meta_'+soil_id+'.csv')
    
    #--- Copy initial soil moisture data and meta to running folder
    copyfile(wd+'/'+wd_sim_db+'/ancillary/initial_sthuf_'+run_id+'.csv',
             wd_run+'/'+wd_sim_db+'/ancillary/initial_sthuf_'+run_id+'.csv')
    
    #--- Copy CO2
    copyfile(wd+'/'+wd_sim_db+'/ancillary/'+co2_data_fn.replace('.dat','.csv'),
             wd_run+'/'+wd_sim_db+'/ancillary/'+co2_data_fn.replace('.dat','.csv'))