# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:27:47 2020

@author: muril
"""

def gen_jules_run(run_id      : str,
                  base_nml_fn : str,
                  driv_id     : str,
                  soil_id     : str,
                  crop_id     : str,
                  crop_nm     : str,
                  wd          : str,
                  wd_sim_db   : str,
                  wd_run      : str,
                  templ_path  : str,
                  verb        = True,
                  upd_base_nml= None,
                  copy_sim_db = False,
                  gen_driving = True, 
                  f_calibrate = False,
                  calib_setup_fn = None):
    
    #-----------------------------------------------------------#
    #---------------------- gen_jules_run ----------------------# 
    #-----------------------------------------------------------#
    #--- Goal: 
    #---    Create Running Environment for JULES namelist
    #--- Parameters: 
    #---    run_id          : Running ID code
    #---    base_nml_fn     : Filename for the base configuration file (CSV) 
    #---    driv_id         : ID for driving data
    #---    soil_id         : ID for soil data
    #---    crop_id         : ID for crop data
    #---    crop_nm         : Crop name
    #---    wd              : Working directory
    #---    verb            : Verbose (boolean)
    #---    upd_base_nml    : Updated base namelist filename
    #---    copy_sim_db     : Flag to copy sim_db CSV data to jules_run
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    #--- Load libs
    import os
    import pandas       as pd
    import gen_nml_defs as gn
    import gen_dat_defs as gd
    import util         as u
    import py_jules_constants as c
    from time import gmtime, strftime, time
    
    #--- Track progress
    start_time = time()
    
    if verb: print('\n!-----------------------------------------!'+
                   '\n!--- Creating jules_run for ID: '+run_id+' ---!'+
                   '\n!-----------------------------------------!\n')
    
    #--- Logs Warning
    warn_msg   = ['Warning Logs for jules_run creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    
    #--- Create/Update "jules_run" folder into the provided working directory (wd)
    if verb: print('Updating Running Directory for ID: '+run_id)
    gn.mk_jules_run(wd_run)
    
    #--------------------------#
    #--- Generate namelists ---#
    #--------------------------#
    
    #--- Update base nml
    if type(upd_base_nml) == type(None):
        #--- Update base template run
        if verb: print('Updating Base Template for ID: '+run_id)
        gn.update_nml_setup(wd+'/'+wd_sim_db+'/'+base_nml_fn,
                            wd+'/'+wd_sim_db+'/driving/meta_'+driv_id+'.csv',
                            wd+'/'+wd_sim_db+'/soil/meta_'+soil_id+'.csv',
                            wd+'/'+wd_sim_db+'/crop/meta_'+crop_id+'.csv',
                            wd+'/'+wd_sim_db+'/meta_'+run_id+'.csv',
                            wd_run+'/nml_setup_'+run_id+'.csv')
        
        #--- Updated base nml name
        upd_base_nml_fn = wd_run + '/nml_setup_'+run_id+'.csv'
        
    else:
        #--- Updated base nml name is provided
        upd_base_nml_fn = upd_base_nml      
        
    #--- Read updated base nml
    base_nml = u.df_csv(upd_base_nml_fn)
    
    #--- Update parameters is calibration step
    if f_calibrate:
        
        if verb: print('Updating Base Template with calibration parameters for ID: '+run_id)
        
        #--- Open calibration setup CSV file
        calib_setup = u.df_csv(calib_setup_fn)
        
        #--- filter based on calibrate flag
        calib_upd   = calib_setup[:][calib_setup['calibrate']]
        
        #--- drop duplicates
        calib_upd   = calib_upd.drop_duplicates()
        
        #--- get last step
        calib_upd.val = calib_upd.last_step
        
        #--- merge with nml base        
        merged_base_nml = pd.merge(base_nml,
                                   calib_upd,
                                   how = 'left',
                                   left_on = ['variable', 'namelist', 'array_id', 'n_nl'],
                                   right_on = ['variable', 'namelist', 'array_id', 'n_nl'],
                                   suffixes=('', '_calib'))
        #--- update values
        merged_base_nml.loc[~merged_base_nml['last_step'].isnull(),'val'] = merged_base_nml.loc[~merged_base_nml['last_step'].isnull(),'val_calib']
        
        #--- update df
        base_nml = merged_base_nml[base_nml.keys()]
        
        #--- write to file
        base_nml.to_csv(upd_base_nml_fn, index = None, header=True)
            
    #--- Create Namelists based on updated nml_setup
    if verb: print('Creating Namelists files for ID: '+run_id)
    gn.gen_nml(upd_base_nml_fn,             # Input namelists setup
               wd+templ_path,               # Folder where templates are
               wd_run+'/namelists')         # Output folder for generated namelists files
    
    #-----------------------------#
    #--- Generate driving data ---#
    #-----------------------------#
    
    if gen_driving:
        #--- Get driving meta data from the updated namelists
        datetime_ini = base_nml['val'][(base_nml['namelist'] == 'jules_drive') & (base_nml['variable'] == 'data_start')].values[0]
        dt           = base_nml['val'][(base_nml['namelist'] == 'jules_drive') & (base_nml['variable'] == 'data_period')].values[0]
        
        #--- list of driving variables and formats
        l_driv_data        = base_nml[['array_id','val']][(base_nml['namelist'] == 'jules_drive') & (base_nml['variable'] == 'var')].sort_values(by=['array_id'])    
        l_driv_data['val'] = l_driv_data['val'].str.replace("'","") # Remove "'" used for Fortran namelists
        
        #--- join formats
        l_driv_data = pd.merge(l_driv_data, c.fmt_driv_jules, on='val')
        
        #--- get driving filename
        driv_out_fn = base_nml['val'][(base_nml['namelist'] == 'jules_drive') & (base_nml['variable'] == 'file')].values[0].split('/')[-1]
        driv_out_fn = driv_out_fn.replace("'","")
        
        #--- Check DB consistency
        if driv_out_fn.split('.')[0] != driv_id:
            msg = 'Warning: Driving ID differs between dashboard and meta_'+driv_id+'.csv'
            print(msg)
            warn_msg.append(msg)
        
        #--- Generate driving data
        if verb: print('Generating Driving Data for ID: '+run_id)
        gd.gen_driving(wd+'/'+wd_sim_db+'/driving/data_'+driv_id+'.csv',
                       datetime_ini,
                       dt,
                       l_driv_data['val'].values.tolist(),
                       l_driv_data['fmt'].values.tolist(),
                       wd_run+'/namelists/data/'+driv_out_fn)
    
    #--------------------------#
    #--- Generate soil data ---#
    #--------------------------#
    
    #--- Get soil data
    soil_out_fn = base_nml['val'][(base_nml['namelist'] == 'jules_soil_props') & (base_nml['variable'] == 'file')].values[0].split('/')[-1]
    soil_out_fn = soil_out_fn.replace("'","")
    
    #--- multi-layers?
    f_ml = base_nml['val'][(base_nml['namelist'] == 'jules_soil_props') & (base_nml['variable'] == 'const_z')].values[0]    
    f_ml = not gn.fortran_bool(f_ml)
    
    #--- Check DB consistency
    if soil_out_fn.split('.')[0] != soil_id:
        msg = 'Warning: Soil ID differs between dashboard and meta_'+soil_id+'.csv'
        print(msg)
        warn_msg.append(msg)
    
    #--- Generate soil data
    if verb: print('Generating Soil Data for ID: '+run_id)
    gd.gen_soil_props(setup_fn = wd+'/'+wd_sim_db+'/soil/data_'+soil_id+'.csv',
                      out_fn   = wd_run+'/namelists/data/'+soil_out_fn,
                      ml       = f_ml)
    
    #-----------------------------#
    #--- Initial soil moisture ---#
    #-----------------------------#
    
    init_shuf_fn = base_nml['val'][(base_nml['namelist'] == 'jules_initial') & (base_nml['variable'] == 'file')].values[0].split('/')[-1]
    init_shuf_fn = init_shuf_fn.replace("'","")    
    
    #--- number of soil layers
    n_layers = int(base_nml['val'][(base_nml['namelist'] == 'jules_soil') & (base_nml['variable'] == 'sm_levels')].values[0])
    
    #--- get field capacity from soil.dat (sm_crit)
    soil_data_csv = u.df_csv(wd+'/'+wd_sim_db+'/soil/data_'+soil_id+'.csv')        
    sm_wilt = soil_data_csv.loc[soil_data_csv['variable'] == 'sm_wilt','val'].values
    sm_crit = soil_data_csv.loc[soil_data_csv['variable'] == 'sm_crit','val'].values
    sm_sat  = soil_data_csv.loc[soil_data_csv['variable'] == 'sm_sat','val'].values
    
    #--- get fraction of sat correspondent to sm_crit
    #sm_crit_frac = (sm_crit + sm_wilt) * 0.5 / sm_sat
    sm_crit_frac = sm_crit / sm_sat # using sm_crit as default
    
    #--- check if soil is homogeneous
    if len(sm_crit_frac) == 1:        
        sm_crit_frac = [sm_crit_frac[0]] * n_layers
        
    #--- Read init soil moisture
    try:        
        init_shuf    = u.df_csv(wd+'/'+wd_sim_db+'/ancillary/initial_sthuf_'+run_id+'.csv')
        if len(init_shuf['layer']) != n_layers:
            print('Warning: Number of soil layers in initial water provided ('+str(len(init_shuf['layer']))+') differs from the number of soil layers (sm_levels='+str(n_layers)+').\n --- Saturation will be assumed for all layers --- ')
            init_shuf = pd.DataFrame({"layer": range(1,n_layers+1),
                                  "init_sthuf": sm_crit_frac})
    except:        
        print('Warning: No initial soil moisture file found in "'+wd+'/'+wd_sim_db+'/ancillary/"'+"\n --- Saturation will be assumed for all layers --- ")        
        init_shuf = pd.DataFrame({"layer": range(1,n_layers+1),
                                  "init_sthuf": sm_crit_frac})
            
    #--- Create initial soil moisture
    if verb: print('Generating Initial Soil Moisture Data for ID: '+run_id)
    gd.gen_init_wat(init_shuf['init_sthuf'].values,
                    wd_run+'/namelists/data/'+init_shuf_fn)
    
    #---------------------------#
    #--- Get prescribed data ---#
    #---------------------------#    
    n_presc      = int(base_nml['val'][(base_nml['namelist'] == 'jules_prescribed') & (base_nml['variable'] == 'n_datasets')].values[0])
    l_presc      = base_nml['val'][(base_nml['namelist'] == 'jules_prescribed_dataset') & (base_nml['variable'] == 'file')].values
    l_presc      = list(set(l_presc)) # unique values   
    
    for i in range(0,n_presc):
        presc_dt_fn = l_presc[i].split('/')[-1]
        presc_dt_fn = presc_dt_fn.replace("'","")
        
        n_nl        = base_nml['n_nl'][(base_nml['namelist'] == 'jules_prescribed_dataset') & (base_nml['val'] == l_presc[i])].values[0]
        var_name    = base_nml['val'][(base_nml['namelist'] == 'jules_prescribed_dataset') & (base_nml['variable'] == 'var') & (base_nml['n_nl'] == n_nl)].values[0].replace("'","")
        p           = base_nml['prec'][(base_nml['namelist'] == 'jules_prescribed_dataset') & (base_nml['variable'] == 'var') & (base_nml['n_nl'] == n_nl)].values[0]
        
        if var_name in ['lai','canht']:
            ndim = 9
        else:
            ndim = 1
        
        #--- Generate presc data
        if verb: print('Generating prescribed ('+presc_dt_fn+') Data for ID: '+run_id)
        gd.gen_presc_dat(wd+'/'+wd_sim_db+'/ancillary/'+presc_dt_fn.replace('.dat','.csv'),
                         var_name,
                         out_fn = wd_run+'/namelists/data/'+presc_dt_fn,
                         p = p,
                         ndim = ndim)
    
    #----------------------------------#
    #--- Create tile fraction array ---#
    #----------------------------------#
    
    if crop_nm == 'Sugarcane' or crop_nm == 'Sorghum':
        # *** Patch for Sugarcane and Sorghum:
        # *** Both will be run as the Maize tile
        crop_nm_tl = 'Maize'
    else:
        crop_nm_tl = crop_nm
    
    #--- Assuming only one crop per simulation
    n_tf = len(c.n_tile_frac['crop'])
    tf   = [0] * n_tf   
    tf[c.n_tile_frac['n_id'][c.n_tile_frac['crop'] == crop_nm_tl].values[0]-1] = 1.
    
    #--- tile fraction filename
    tf_nm = base_nml['val'][(base_nml['namelist'] == 'jules_frac') & (base_nml['variable'] == 'file')].values[0].split('/')[-1]
    tf_nm = tf_nm.replace("'","")
    
    #--- Generate tile fraction file
    if verb: print('Generating Tile Fraction Data for ID: '+run_id)
    gd.gen_tile_frac(tf,
                     wd_run+'/namelists/data/'+tf_nm)
    
    #------------------------------------------#
    #--- Generate required data for TRIFFID ---#
    #------------------------------------------#
    if base_nml['val'][(base_nml['namelist'] == 'jules_biocrop') & (base_nml['variable'] == 'file')].values[0] != "''":
        hv_doy_nm = base_nml['val'][(base_nml['namelist'] == 'jules_biocrop') & (base_nml['variable'] == 'file')].values[0].split('/')[-1]
        hv_doy_nm = hv_doy_nm.replace("'","")
    
        #--- Generate harvest doy
        if verb: print('Generating Harvest DOY Data for ID: '+run_id)       
        
        #--- get the harvest doy from updated base
        array_id_doy = base_nml['array_id'][(base_nml['namelist'] == 'jules_crop_props') & (base_nml['val'] == "'croplatestharvdate'")].values[0]
        hv_doy = base_nml['val'][(base_nml['namelist'] == 'jules_crop_props') & (base_nml['variable'] == "const_val") & (base_nml['array_id'] == array_id_doy)].values[0]
        hv_doy = int(hv_doy)
        
        #--- get the number of pft
        npft = base_nml['val'][(base_nml['namelist'] == 'jules_surface_types') & (base_nml['variable'] == "npft")].values[0]
        npft = int(npft)
        
        #--- replicate harvest doy as vector of npft
        hv_doy = [hv_doy] * npft
        
        #--- create the file
        gd.gen_harv_doy(hv_doy,
                        wd_run+'/namelists/data/'+hv_doy_nm)
        
    if copy_sim_db:        
        #----------------------#
        #--- Backup all CSV ---#
        #----------------------#            
        #--- This is useful for sensitivity analysis        
        gn.backup_sim_db(run_id,
                         crop_id,
                         driv_id,
                         soil_id,
                         presc_dt_fn,
                         wd,
                         wd_run,
                         base_nml_fn,
                         wd_sim_db = wd_sim_db)       
                
    #--- Check progression
    if len(warn_msg) > 1:
        
        #--- Warnings found
        print('jules_run created succesfully, but some warnings were generated and can be found at file: warnings_gen_jules_run.wng')
        with open('warnings_gen_jules_run.wng', 'w') as f:
            for item in warn_msg:
                f.write("%s\n" % item)
                
    else:
        #--- No Warnings
        print('jules_run created succesfully!')
        if os.path.exists('warnings_gen_jules_run.wng'):
            os.remove('warnings_gen_jules_run.wng')    
    
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))
    
    return(base_nml)
