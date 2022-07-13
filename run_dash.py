# -*- coding: utf-8 -*-
"""
    #----------------#
    #--- run_dash ---#
    #----------------#
    
    #--- This script was developed to run the JULES-crop for the specific sites 
    #--- flagged with run_jules=TRUE in the dashboard_db.csv file.
    #--- If fields observations for a given field is placed in obs_db path,
    #--- a model performance is calculated for every site and overall pooled.
    
    #--- Murilo Vianna (murilodsv@gmail.com)
    #--- Feb, 2020.
    #--- Dev-log in: https://github.com/Murilodsv/py-jules

"""

#------------------------#
#--- Running Settings ---#
#------------------------#
sim_id      = 'pj_run'
dash_nm     = 'dashboard_db.csv'        # Filename of Dashboard CSV 
meta_nm     = 'meta_var.csv'            # Filename of Meta-info CSV 
calc_perf   = True                      # Flag to Calculate model performance
clean_res   = True                      # Flag to Get clean results
save_res    = True                      # Flag to save results in 'results' folder
save_all    = False                     # Flag to save all simulations files in 'results' folder
res_CSV     = True                      # Flag to save simulation results as CSV files
ftime_idx   = True                      # Flag to compute time indexers in simulation results (e.g. date, year, doy)
verb        = True                      # Flag for verbose
exec_fn     = 'jules.exe'               # JULES executable filename
exec_path   = 'jules_run'               # folder where simulations will be run
templ_path  = '/templates/versions/r16801_biocrop'
f_plot_perf = True                      # Plot performance
f_calibrate = False                     # Calibration Flag
calib_setup_fn = 'calibration_setup.csv'
wipe_res   = False                      # Flag to wipe results [useful to clean-up calibration comparison]
compare_res= False
calib_dash = False

#----------------------#
#--- Load libraries ---#
#----------------------#
import os
import util         as u
import numpy        as np
from py_jules_run import py_jules_run
from time import time

#--- Track progress
run_start = time()
    
#----------------------#
#--- Read dashboard ---#
#----------------------#

#--- get run wd
wd   = os.getcwd().replace('\\','/')

#--- Open CSVs
dash = u.df_csv(wd+'/'+dash_nm)
meta = u.df_csv(wd+'/'+meta_nm)

#--- Get scripts arguments
if __name__ == "__main__":
    import sys    
    if len(sys.argv) > 1:
        #--- Filter sites and sim_id based on arguments
        arg_run_id = np.array(str(sys.argv[1]).split(',')) # arg_run_id = np.array(str('SC3572').split(','))
        sim_id     = str(sys.argv[2])
        
        if len(sys.argv) == 4: 
            #--- dashboard provided as argument
            dash_nm = str(sys.argv[3])
            dash = u.df_csv(wd+'/'+dash_nm)
        
        if len(sys.argv) == 6:                        
            #--- check if this is a calibration routine
            f_calibrate = str(sys.argv[3]).lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
                
            #--- turn-off plots during calibration procedure to gain performance
            if f_calibrate: 
                f_plot_perf    = False 
                calib_setup_fn = str(sys.argv[4])
                compare_res    = str(sys.argv[5]).lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
                                
                #--- read calibration setup
                calib_setup = u.df_csv(calib_setup_fn)
                
                #--- filter based on calibrate flag
                calib_upd = calib_setup[:][calib_setup['calibrate']]
                
                #--- check whether there are dashboard values to optimize
                if any(calib_upd['file'] == 'dashboard_db.csv'):
                    calib_dash = True
                    calib_setup_dash = calib_upd[:][calib_upd['file'] == 'dashboard_db.csv']
                    for c,i in zip(calib_setup_dash.variable, calib_setup_dash.namelist):
                        
                        #--- get type and precision
                        type_val = str(calib_setup_dash.loc[(calib_setup_dash['variable'] == c) & (calib_setup_dash['namelist'] == i),'type'])                        
                        prec_val = int(calib_setup_dash.loc[(calib_setup_dash['variable'] == c) & (calib_setup_dash['namelist'] == i),'prec'])
                        
                        #--- get the new value
                        rep_val  = calib_setup_dash.loc[(calib_setup_dash['variable'] == c) & (calib_setup_dash['namelist'] == i),'last_step'].values[0]
                        
                        #--- convert to int or flt
                        if type_val.lower() in ['integer', 'int', 'i']:
                            rep_val = int(rep_val)
                        else:
                            rep_val = round(rep_val, prec_val)
                            
                        #--- update dashboard
                        dash.loc[dash['run_id'] == i,c] = rep_val
                                
        #--- modify dash for comparison run
        if compare_res:
            
            #--- switch-on plots
            f_plot_perf    = True
            
            #--- pass f_calibrate internally to dash ---#
            dash['f_calibrate'] = False
            dash['wipe_res']    = False
                        
            #--- copy lines for "c" suffix
            dash_c = dash.loc[np.isin(dash['run_id'],arg_run_id),:]
            
            #--- add suffix to run_id
            run_idc = np.array([sub + 'c' for sub in arg_run_id])
            
            #--- set the calibration flags and wipe data
            dash_c.loc[:,'f_calibrate'] = True
            dash_c.loc[:,'wipe_res']    = True
            dash_c.loc[:,'run_id']      = run_idc
                        
            #--- append 'c' ids to arguments
            arg_run_id = np.append(arg_run_id, run_idc)            
            
            #--- append to dash
            if calib_dash: dash = u.df_csv(wd+'/'+dash_nm)                
            dash = dash.append(dash_c)            
        
        #--- Update Flags
        dash['run_jules'] = False
        dash.loc[np.isin(dash['run_id'],arg_run_id),'run_jules'] = True
        print('Running with provided arguments:\n   -> '+str(sys.argv[1])+'\n   -> '+str(sys.argv[2]))

#--- Filter sites flagged to run
dash_run = dash[:][dash['run_jules']]

#--- Create py-jules meta files
if any(dash_run['gen_meta']):
    import gen_dat_defs as gd
    gd.gen_dash_meta(dash_run,
                     wd_o    = '/sim_db')

#--- Initalize results
all_res = {}
all_per = {}
init_res= True
perf_success = False

#--- Run for all treatments
for run_id in dash_run['run_id']:
    
    #--- Track progress
    run_id_st = time()
    
    base_nml_fn     = dash_run['sim_base'][dash_run['run_id'] == run_id].values[0]
    driv_id         = dash_run['driv_id'][dash_run['run_id']  == run_id].values[0]
    soil_id         = dash_run['soil_id'][dash_run['run_id']  == run_id].values[0]
    crop_id         = dash_run['crop_id'][dash_run['run_id']  == run_id].values[0]
    crop_nm         = dash_run['crop_nm'][dash_run['run_id']  == run_id].values[0] 
    
    #--- check if this is a calibration comparison
    if compare_res:        
        #--- get calibration flags
        f_calibrate = dash_run['f_calibrate'][dash_run['run_id'] == run_id].values[0]
        wipe_res    = dash_run['wipe_res'][dash_run['run_id'] == run_id].values[0]
    
    if 'templ_path' in dash_run.keys(): templ_path = dash_run['templ_path'][dash_run['run_id']  == run_id].values[0]    
        
    #--- running path
    wd_run = wd + '/'+exec_path+'/' + run_id
    
    #--------------------#
    #--- Run py-JULES ---#
    #--------------------#
    res = py_jules_run(run_id,
                       base_nml_fn,
                       driv_id,
                       soil_id,
                       crop_id,
                       crop_nm,
                       wd,
                       'sim_db',
                       wd_run,
                       exec_fn,
                       templ_path,
                       verb     = verb,
                       res_CSV  = res_CSV,
                       time_idx = ftime_idx,
                       clean_res= clean_res,
                       f_calibrate = f_calibrate,
                       calib_setup_fn = calib_setup_fn)
    
    #--- If simulations went into any error skip this run_id
    #if type(res) == type(None): continue
        
    #--- Compute performance?
    if calc_perf:        
        import get_model_perf as mp               
        
        #---------------------------------#
        #--- Compute model performance ---#
        #---------------------------------#
        run_perf = mp.get_mp(run_id,
                             wd,
                             wd_run,
                             meta,
                             res,
                             dash_run,
                             setup_nml = u.df_csv(wd_run+'/nml_setup_'+run_id+'.csv'),
                             obs_type  = 'avg',
                             time_idx  = ['year','doy','dap','das','date'],
                             merge_idx = ['year','doy','sim_code'],
                             save_res  = True)
        
        if run_perf[str(run_id)+'.status'] == 0:
            
            #--- append performance if has no error
            all_per = {**all_per, **run_perf}
            
            if f_plot_perf:
                #------------------------#
                #--- Plot performance ---#
                #------------------------#            
                df_plot = mp.plot_perf(run_id,
                                       run_perf,
                                       x_nm   = 'dap',        # X-axis
                                       fv_nm  = 'label_var',  # Facets
                                       fn_out = wd_run+'/namelists/output/'+str(run_id),
                                       l_p_idx = ['r2','d','ef','rmse'],
                                       size_p   = 5)                            
                
                if init_res:
                    df_plot_all = df_plot
                else:
                    df_plot_all = df_plot_all.append(df_plot)
            else:
                #--- plotting is turned off
                df_plot_all = None
            
            #--- To flag that at least one site got performance ran
            perf_success = True
                
        else:
            print('Warning: No observed data for this site or dates do not match for any of observations.\n --- Please check if simulation dates match with observations ---')
    
    #--- Store all results
    all_res = {**all_res, **res}
    
    #--- save results
    #if save_res: gn.save_res(wd, run_id, save_all)
    
    #--- update flags
    if init_res: init_res = False
    
    #--- track time
    print("\nElapsed time of ID "+str(run_id)+": --- %.3f seconds ---" % (time() - run_id_st))

#--- Compute overall performance
if calc_perf and perf_success:
    mp.get_mp_all(sim_id,
                  all_per,
                  df_plot_all,
                  wd,
                  v_f      = 'variable',
                  save_res = True,
                  x_nm     = 'dap',
                  y_nm     = 'value',
                  fv_nm    = 'label_var',
                  hue_nm   = 'run_id',
                  fn_out   = wd + '/'+exec_path+'/'+sim_id,
                  size_p   = 5,
                  f_plot_perf = f_plot_perf)
    
#--- track time
print("\nElapsed time of simulation "+str(sim_id)+": --- %.3f seconds ---" % (time() - run_start))

