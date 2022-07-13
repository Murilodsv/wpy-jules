# -*- coding: utf-8 -*-
"""
    #----------------#
    #--- run_sens ---#
    #----------------#
    
    #--- This script was developed to run a local sensitivity analysis for 
    #--- JULES-crop for the specific sites flagged with run_jules=TRUE in the 
    #--- sensitivity_run_setup.csv file. The file sensitivity_par_range.csv 
    #--- controls the parameters range for sensitivity.
    
    #--- If a list of run_id is provided in the script argument the run_jules
    #--- flags are set to the provided list. This is useful to run multiple 
    #--- run_ids is parallel jobs. Example:
    
    #--- The below call will run only for run_ids MZ0002 and MZ0099
    $ python run_sens.py MZ0002,MZ0099 
    
    #--- Murilo Vianna (murilodsv@gmail.com)
    #--- Feb, 2020.

"""

#------------------------#
#--- Running Settings ---#
#------------------------#

#--- Every line of dash_nm that has the column 'run_sens' set to True will be used as a baseline in the sensitivity analysis
dash_nm     = 'sensitivity_run_setup.csv'       # Filename of Dashboard CSV
meta_nm     = 'meta_var.csv'                    # Filename of Meta-info CSV 
calc_perf   = True                              # Flag to Calculate model performance
clean_res   = True                              # Flag to Get clean results
save_res    = True                              # Flag to save results in 'results' folder
save_all    = False                             # Flag to save all simulations files in 'results' folder
res_CSV     = True                              # Flag to save simulation results as CSV files
ftime_idx   = True                              # Flag to compute time indexers in simulation results (e.g. date, year, doy)
verb        = True                              # Flag for verbose
exec_fn     = 'jules.exe'                       # JULES ecxecutable filename
exec_path   = 'jules_run_sens'                  # folder where simulations will be run

#----------------------------#
#--- Sensitivity Settings ---#
#----------------------------#
pace        = 0.2                               # Pace within sensitivity range (e.g. 0.2 is 20% variation from min to max range)
sens_par_nm = 'sensitivity_par_range.csv'       # Filename of sensitivity parameters range (CSV)
wd_sim_db   = 'sim_db_sens'                     # Name of baseline sim_db folder within results_sens
time_idx    = ['year','doy','dap','das','date'] # Time indexers 
dim_idx     = ['soil','pft','cpft']             # Dimensions indexers

#--- Keys to merge sensitivity & baseline [note that das is not present as we also assess the initial date for simulation start]
merge_col   = ['year','doy','dap','date'] + dim_idx + ['sim_code'] 

#--- Model outputs to analyze sensitivity
sens_vars   = ['cropdvi',
               'croplai',
               'cropcanht',
               'cropharvc',
               'cropreservec',
               'cropstemc',
               'croprootc',
               'cropleafc',
               'resp_r',
               'resp_l',
               'resp_p',
               'gpp',
               'npp',
               'soil_wet',
               't_soil',
               'smcl',
               'le']

#----------------------#
#--- Load libraries ---#
#----------------------#
import os#; os.chdir('C:/Murilo/py-jules')
import shutil
import pandas as pd
import numpy as np

#import gen_nml_defs as gn
import util         as u
from py_jules_run   import py_jules_run
from get_netcdf     import get_res
from get_model_perf import check_dependencies

#----------------------#
#--- Read dashboard ---#
#----------------------#

#--- get run wd
wd   = os.getcwd().replace('\\','/')

#--- Open CSVs
dash = u.df_csv(wd+'/'+dash_nm)
meta = u.df_csv(wd+'/'+meta_nm)
sens = u.df_csv(wd+'/'+sens_par_nm)

#--- Get scripts arguments
if __name__ == "__main__":
    import sys    
    if len(sys.argv) > 1:
        #--- Filter sites based on arguments
        arg_run_id = np.array(str(sys.argv[1]).split(','))
        
        #--- Update Flags
        dash['run_jules'] = False
        dash.loc[np.isin(dash['run_id'],arg_run_id),'run_jules'] = True        

#--- Filter sites flagged to run
dash_run = dash[:][dash['run_jules']]
sens_run = sens[:][sens['run_sens' ]]

#--- Run for all treatments
for run_id in dash_run['run_id']:
    
    #--- Get run data
    base_nml_fn     = dash_run['sim_base'][dash_run['run_id'] == run_id].values[0]
    driv_id         = dash_run['driv_id'][dash_run['run_id']  == run_id].values[0]
    soil_id         = dash_run['soil_id'][dash_run['run_id']  == run_id].values[0]
    crop_id         = dash_run['crop_id'][dash_run['run_id']  == run_id].values[0]
    crop_nm         = dash_run['crop_nm'][dash_run['run_id']  == run_id].values[0]

    #--- running path
    wd_run = wd + '/'+exec_path+'/' + run_id    
    
    #--------------------#
    #--- Run Baseline ---#
    #--------------------#
    res = py_jules_run(run_id,
                       base_nml_fn,
                       driv_id,
                       soil_id,
                       crop_id,
                       crop_nm,
                       wd,
                       'sim_db',
                       wd_run+'/sens_run',
                       exec_fn,
                       verb     = verb,
                       res_CSV  = res_CSV,
                       time_idx = ftime_idx,
                       clean_res= clean_res,
                       upd_base_nml= None,
                       copy_sim_db = True)      # turned on to be used on sensitivity analysis
    
    if type(res) == type(None):
        print('ERROR: Error in Baseline Simulations for ID: '+str(run_id)+'\n -- SIMULATION ABORTED FOR THIS ID -- ')
        continue
    
    #--- Get targeted results from simulations outputs
    res_df_b = get_res(sens_vars,
                       res,
                       time_idx  = time_idx,
                       dim_idx   = dim_idx)
    
    #--- Rename columns
    res_df_b = res_df_b.rename(columns = {'sim_value':'sim_base'})
        
    #--- Save Baseline Results
    #gn.save_sens_res(wd, run_id,save_all = True)
    
    #--- Store baseline sim_db for this run_id
    src = wd_run+'/sens_run/sim_db'
    dst = wd_run+'/sim_db_sens'
    
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(src,dst)
    
    #--- Store baseline base_nml for this run_id
    src = wd_run+'/sens_run/nml_setup_'+run_id+'.csv'
    dst = wd_run    
    shutil.copy(src,dst)
    
    #--- Sensitivity for all parameters
    for i in sens_run.index:
                
        #--- Get sensitivity run class        
        var_class = sens_run['class'][sens_run.index == i].values[0]
        
        #--- get sensitivity run indexers and info
        var = sens_run['variable'][sens_run.index == i].values[0]
        nml = sens_run['namelist'][sens_run.index == i].values[0]
        arr = sens_run['array_id'][sens_run.index == i].values[0]
        nnl = sens_run['n_nl'][sens_run.index == i].values[0]  
        dpc = sens_run['dependency'][sens_run.index == i].values[0]  
        typ = sens_run['type'][sens_run.index == i].values[0]
        
        if var_class == 'parameter':
            
            #-------------------------------------#
            #--- Sensitivity on parameter type ---#
            #-------------------------------------#
            
            #--- Use updated base_nml
            base_nml_fn = wd_run+'/nml_setup_'+run_id+'.csv'
            
            #--- Read base nml
            base_nml = pd.DataFrame(pd.read_csv(base_nml_fn))
                        
            #--- Find on base_nml
            f   = ((base_nml['variable'] == var) & 
                   (base_nml['namelist'] == nml) & 
                   (base_nml['array_id'] == arr) & 
                   (base_nml['n_nl'] == nnl))
            
            #--- check if parameter exist in base simulation
            if not any(f):
                print('Warning: Parameter '+str(var)+' not found in base simulation file: nml_setup_'+str(run_id)+'.csv.\n - PARAMETER IGNORED - ')
                sens_stat = 1
            
            #--- get range thresholds for sensitivity analysis            
            val_min = sens_run['min'][sens_run.index == i].values[0]
            val_max = sens_run['max'][sens_run.index == i].values[0]
            val_pace= pace            
            
            if typ == 'date':
                
                from datetime import datetime                
                
                #--- date-type parameter
                val        = base_nml['val'][f].values[0]
                val_date   = datetime.strptime(val, "'%Y-%m-%d %H:%M:%S'")
                
                range_sens = np.arange(val_min, val_max,(val_max - val_min) * val_pace)
                if not val_max in range_sens: range_sens = np.append(range_sens,val_max)
                
                #--- round days
                range_sens = np.around(range_sens, decimals=0)
                
                #--- Apply timedeltas to baseline date
                range_sens = pd.to_timedelta(range_sens, unit = 'd') + pd.to_datetime(val_date)
                
                #--- convert back to str format
                range_sens = range_sens.strftime("'%Y-%m-%d %H:%M:%S'")
                
            else:
                #--- real-type parameter
                val        = float(base_nml['val'][f].values[0])
                range_sens = np.arange(val_min, val_max,(val_max - val_min) * val_pace)
                if not val_max in range_sens: range_sens = np.append(range_sens,val_max)
                                                                
            init_df_i = True            
            for val_s in range_sens:                
                                
                #--- Check dependency
                if str(dpc) != 'nan':
                    try:
                        val_s = check_dependencies(val_check   = val_s,
                                                   nml_check   = nml,
                                                   arr_check   = arr,                       
                                                   nnl_check   = nnl,
                                                   dpc         = dpc,
                                                   base_nml_fn = base_nml_fn)
                    except:
                        print('Warning: Tried to check dependencies for parameter '+var+' but failed.\n -- Please check dependency rules --')
                
                #--- Get base nml
                base_nml_s = pd.DataFrame(pd.read_csv(base_nml_fn))
                
                #--- update with new value
                base_nml_s.loc[f,'val'] = val_s
                
                #--- save it
                base_nml_s_fn = wd_run+'/nml_setup_'+run_id+'_sens.csv'
                base_nml_s.to_csv(base_nml_s_fn, index = None, header=True)
                
                print("----------\n Running Sensitivity Scenario for Variable: "+str(var)+" with value: "+str(val_s)+"\n----------")

                #--------------------------------#
                #--- Run Sensitivity Scenario ---#
                #--------------------------------#
                res_s = py_jules_run(run_id,
                                     base_nml_fn,
                                     driv_id,
                                     soil_id,
                                     crop_id,
                                     crop_nm,
                                     wd,
                                     exec_path+'/'+run_id+'/'+wd_sim_db,
                                     wd_run+'/sens_run',
                                     exec_fn,
                                     verb        = verb,
                                     res_CSV     = res_CSV,
                                     time_idx    = ftime_idx,
                                     clean_res   = clean_res,
                                     upd_base_nml= base_nml_s_fn,
                                     copy_sim_db = False,
                                     gen_driving = True)
                
                if type(res_s) == type(None):
                    print('Warning: Simulation Error in Simulations Scenario of variable '+str(var)+' for value '+str(val_s)+'\n -- SCENARIO ABORTED -- ')
                    continue
                
                #--- Get targeted results from simulations outputs
                res_df_s = get_res(sens_vars,
                                   res_s,
                                   time_idx  = time_idx,
                                   dim_idx   = dim_idx)
                
                #--- Merge with baseline 
                res_df_m = pd.merge(res_df_b, res_df_s, how = 'left', on = merge_col)
                
                #--- Patch for different dates merging
                if ('das' in time_idx) and (not 'das' in merge_col):                    
                    res_df_m['das'] = res_df_m['das_x']
                    res_df_m = res_df_m.drop(columns = ['das_x','das_y'])
                    
                    #--- order df cols
                    res_df_m[time_idx + 
                             list(res_df_m.keys()[~np.isin(res_df_m.keys(), time_idx)])]
                                    
                #--- Check results
                if len(res_df_m) == 0: 
                    print("Warning: Could not merge baseline and sensitivity scenario of value "+str(val_s)+" for parameter "+str(var)+".\n - SCENARIO RULED OUT - ")
                    continue
                
                if len(res_df_m) != len(res_df_b): 
                    print("Warning: Merging baseline and sensitivity scenario resulted in different df length of value "+str(val_s)+" for parameter "+str(var)+".")
                
                #--- Add parameter values
                res_df_m['sens_var']  = var
                res_df_m['sens_val']  = val_s
                res_df_m['base_val']  = val
                
                #--- Add index
                res_df_m['run_id' ]   = run_id
                
                if init_df_i:
                    res_df    = res_df_m
                    init_df_i = False
                else:
                    res_df    = res_df.append(res_df_m)
                    
            #--- End of sensitivity for parameter var
            res_out_nm = wd_run+'/'+str(run_id)+'.'+str(var)+'.'+str(nml)+'.'+str(arr)+'.'+str(nnl)+'.sens.csv'
            res_df.to_csv(res_out_nm, index = None, header=True)
                        
            print('Running Sensitivity for Parameter '+str(var)+' is Completed!')
        
        elif var_class == 'soil_data':
   
            #-------------------------------------#
            #--- Sensitivity on soil data type ---#
            #-------------------------------------#
            
            #--- read updated base_setup
            base_nml_fn = wd_run+'/nml_setup_'+run_id+'.csv'
            
            #--- read soil data
            soil_dt_fn = wd_run+'/sim_db_sens/soil/data_'+soil_id+'.csv'
            soil_dt    = pd.DataFrame(pd.read_csv(soil_dt_fn))
            
            #--- Update sim_db_sens_data
            dst = wd_run+'/sim_db_sens_data'
            src = wd_run+'/sim_db_sens'
    
            if os.path.exists(dst): shutil.rmtree(dst)
            shutil.copytree(src,dst)

            #--- Find on base_nml
            f   = ((soil_dt['variable'] == var) &                    
                   (soil_dt['array_id'] == arr))
            
            #--- check if parameter exist in base simulation
            if not any(f):
                print('Warning: Parameter '+str(var)+' not found in base simulation file: nml_setup_'+str(run_id)+'.csv.\n - PARAMETER IGNORED - ')
                sens_stat = 1
                        
            #--- get range thresholds for sensitivity analysis            
            val_min = sens_run['min'][sens_run.index == i].values[0]
            val_max = sens_run['max'][sens_run.index == i].values[0]
            val_pace= pace            
            
            if typ == 'date':
                
                from datetime import datetime                
                
                #--- date-type parameter
                val        = base_nml['val'][f].values[0]
                val_date   = datetime.strptime(val, "'%Y-%m-%d %H:%M:%S'")
                
                range_sens = np.arange(val_min, val_max,(val_max - val_min) * val_pace)
                if not val_max in range_sens: range_sens = np.append(range_sens,val_max)
                
                #--- round days
                range_sens = np.around(range_sens, decimals=0)
                
                #--- Apply timedeltas to baseline date
                range_sens = pd.to_timedelta(range_sens, unit = 'd') + pd.to_datetime(val_date)
                
                #--- convert back to str format
                range_sens = range_sens.strftime("'%Y-%m-%d %H:%M:%S'")
                
            else:
                #--- real-type parameter
                val        = float(soil_dt['val'][f].values[0])
                range_sens = np.arange(val_min, val_max,(val_max - val_min) * val_pace)
                if not val_max in range_sens: range_sens = np.append(range_sens,val_max)
                                                                
            init_df_i = True
            for val_s in range_sens:                
                                
                #--- Check dependency
                if str(dpc) != 'nan':
                    try:
                        val_s = check_dependencies(val_check   = val_s,
                                                   nml_check   = nml,
                                                   arr_check   = arr,                       
                                                   nnl_check   = nnl,
                                                   dpc         = dpc,
                                                   base_nml_fn = base_nml_fn)
                    except:
                        print('Warning: Tried to check dependencies for parameter '+var+' but failed.\n -- Please check dependency rules --')
                
                #--- Get base nml
                soil_dt_s    = pd.DataFrame(pd.read_csv(soil_dt_fn))
                
                #--- update with new value
                soil_dt_s.loc[f,'val'] = val_s
                
                #--- save into the sim_db_sens_data
                soil_dt_s_fn = wd_run+'/sim_db_sens_data/soil/data_'+soil_id+'.csv'
                soil_dt_s.to_csv(soil_dt_s_fn, index = None, header=True)
                
                #--- use the same namelist setup of baseline scenario as only soil data has changed
                base_nml_s_fn = base_nml_fn
                
                print("----------\n Running Sensitivity Scenario for Variable: "+str(var)+" with value: "+str(val_s)+"\n----------")

                #--------------------------------#
                #--- Run Sensitivity Scenario ---#
                #--------------------------------#
                res_s = py_jules_run(run_id,
                                     base_nml_fn,
                                     driv_id,
                                     soil_id,
                                     crop_id,
                                     crop_nm,
                                     wd,
                                     exec_path+'/'+run_id+'/'+wd_sim_db+'_data',
                                     wd_run+'/sens_run',
                                     exec_fn,
                                     verb        = verb,
                                     res_CSV     = res_CSV,
                                     time_idx    = ftime_idx,
                                     clean_res   = clean_res,
                                     upd_base_nml= base_nml_s_fn,
                                     copy_sim_db = False,
                                     gen_driving = True)
                
                if type(res_s) == type(None):
                    print('Warning: Simulation Error in Simulations Scenario of variable '+str(var)+' for value '+str(val_s)+'\n -- SCENARIO ABORTED -- ')
                    continue
                
                #--- Get targeted results from simulations outputs
                res_df_s = get_res(sens_vars,
                                   res_s,
                                   time_idx  = time_idx,
                                   dim_idx   = dim_idx)
                
                #--- Merge with baseline 
                res_df_m = pd.merge(res_df_b, res_df_s, how = 'left', on = merge_col)
                
                #--- Patch for different dates merging
                if ('das' in time_idx) and (not 'das' in merge_col):                    
                    res_df_m['das'] = res_df_m['das_x']
                    res_df_m = res_df_m.drop(columns = ['das_x','das_y'])
                    
                    #--- order df cols
                    res_df_m[time_idx + 
                             list(res_df_m.keys()[~np.isin(res_df_m.keys(), time_idx)])]
                                    
                #--- Check results
                if len(res_df_m) == 0: 
                    print("Warning: Could not merge baseline and sensitivity scenario of value "+str(val_s)+" for parameter "+str(var)+".\n - SCENARIO RULED OUT - ")
                    continue
                
                if len(res_df_m) != len(res_df_b): 
                    print("Warning: Merging baseline and sensitivity scenario resulted in different df length of value "+str(val_s)+" for parameter "+str(var)+".")
                
                #--- Add parameter values
                res_df_m['sens_var']  = var
                res_df_m['sens_val']  = val_s
                res_df_m['base_val']  = val
                
                #--- Add index
                res_df_m['run_id' ]   = run_id
                
                if init_df_i:
                    res_df    = res_df_m
                    init_df_i = False
                else:
                    res_df    = res_df.append(res_df_m)
                    
            #--- End of sensitivity for parameter var
            res_out_nm = wd_run+'/'+str(run_id)+'.'+str(var)+'.'+str(nml)+'.'+str(arr)+'.'+str(nnl)+'.sens.csv'
            res_df.to_csv(res_out_nm, index = None, header=True)
                        
            print('Running Sensitivity for Parameter '+str(var)+' is Completed!')
            
        else:
            
            #--------------------------------#
            #--- Sensitivity on data type ---#
            #--------------------------------#
            
            print('Running Sensitivity for Data ') 
            
        
    print('Sensitivity run for ID: '+str(run_id)+' is completed!')

