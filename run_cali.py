# -*- coding: utf-8 -*-
"""
    #----------------#
    #--- run_cali ---#
    #----------------#
    
    #--- Murilo Vianna (murilodsv@gmail.com)
    #--- Feb, 2021.
    #--- Dev-log in: https://github.com/Murilodsv/py-jules

"""
# DEBUG import os; os.chdir('C:/Murilo/py-jules')

#----------------------#
#--- Load libraries ---#
#----------------------#
import os
import util              as u
import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt
import random
from time import time
from subprocess import run
from scipy.optimize import minimize

#--- Default setups
prec_obj_fun       = 4 
ini_calib_setup_fn = 'calibration_setup.csv'

#--- Track progress
run_start = time()

#--- Get scripts arguments
if __name__ == "__main__":
    import sys    
    if len(sys.argv) == 8:
        #--- Filter sites and sim_id based on arguments
        arg1     = str(sys.argv[1]) #debug arg1 = 'SC1075,SC1076'
        arg2     = str(sys.argv[2]) #debug arg2 = 'calib_test'
        arg3     = str(sys.argv[3]) #debug arg3 = 'T'
        arg4     = str(sys.argv[4]) #debug arg4 = 'et,gpp'
        arg5     = str(sys.argv[5]) #debug arg5 = 'd'
        arg6     = str(sys.argv[6]) #debug arg6 = 'calibration_setup.csv'
        arg7     = str(sys.argv[7]) #debug arg7 = 'T'
        
        #---store minimize option
        f_minimize         = arg3.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']        
        
        #--- keep arg3 = T
        #--- if this script is calling run_dash it must keep arg3 = T
        #--- arg7 will tell whether it should be a comparison or not
        arg3               = 'T' 
        
        #--- get other arguments
        target_var         = np.array(arg4.split(','))
        stat_index         = arg5
        ini_calib_setup_fn = arg6
        compare_res        = arg7.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
    else:
        print('Missing arguments: Please provide the exact number of arguments for calibration.')
        
#--- get run wd
wd   = os.getcwd().replace('\\','/')

#--- Function that calculates py-jules performance
def perf_dash(p,
              std_penalty = 1e6,
              plot_tracker= True,
              compare_res = False):
    
    #--- arg1           : global input var
    #--- arg2           : global input var
    #--- arg3           : global input var
    #--- target_var     : global input var
    #--- stat_index     : global input var
    #--- prec_obj_fun   : global input var
    #--- calib_setup_fn : global input var
    
    #--- read calibration setup
    calib_setup = u.df_csv(calib_setup_fn)
    
    #--- filter only calibrate parameters
    calib_setup = calib_setup[:][calib_setup.calibrate]
    
    #--- re-scale parameters
    calib_setup.last_step = np.array(calib_setup.min_v + (calib_setup.max_v - calib_setup.min_v) * p).round(max(calib_setup.prec))
    
    #--- store last-step in calib
    calib_setup.calib = calib_setup.last_step
    
    #--- calculate penalization in case of error or out-of-bound parameters
    obj_fun_p = round(std_penalty * random.randint(100,110) / 100, prec_obj_fun)
    
    #--- consolidate iteration
    if any(i > 1 for i in p) or any(i < 0 for i in p):        
        #--- penalize        
        print('Warning: Iteration out of bounds 0-to-1\n --- Objective fun penalized ---')
        return(obj_fun_p)
        
    #--- re-write parameters
    calib_setup.to_csv(calib_setup_fn, index = None, header=True)
    
    #--- generate batch call
    b_call = 'python run_dash.py '+arg1+' '+arg2+' '+arg3+' '+calib_setup_fn+' '+str(compare_res)
        
    #--- Prepare running args
    run_args = ['cd '+wd,                                       # get into root
                  b_call]                                       # run run_dash with arguments for calibration
    
    #--------------------#
    #--- Run py-jules ---#
    #--------------------#
    try:
        res = run("; ".join(run_args), shell = True)    
        if not res.returncode == 0:    
            print('Error: Simulation error! \n --- Objective fun penalized ---')            
            return(obj_fun_p)
    except:        
        class res:
            returncode = 1
    
    if not res.returncode == 0:    
            print('Error: Simulation error! \n --- Objective fun penalized ---')            
            return(obj_fun_p)
            
    #--- read performance
    calib_perf = u.df_csv(wd+'/jules_run/'+arg2+'.model_performance.csv')    
    
    #--- use only the ensemble
    calib_perf = calib_perf[:][calib_perf['run_id'] == 'ensemble']    
    
    #--- get objective function
    obj_fun = np.mean(calib_perf[calib_perf.model.isin(target_var)][stat_index])
    
    if stat_index.lower() in ['ef', 'r', 'r2', 'd', 'cc']:
        #--- maximize towards 1
        obj_fun = 1 - obj_fun
    
    #--- round obj_fun
    #--- Note: this helps to gain performance
    obj_fun = round(obj_fun, prec_obj_fun)
    
    #--- update calibration tracker    
    it_tracker         = u.df_csv(wd+'/jules_run/'+arg2+'.calibration_tracker.csv')
    it                 = len(it_tracker.iteration)    
    it_tracker.loc[it] = np.append([it, obj_fun], np.array(calib_setup.last_step))
    it_tracker.to_csv(wd+'/jules_run/'+arg2+'.calibration_tracker.csv', index = None, header=True)
    
    #--- plot tracker
    if plot_tracker:        
        plt.rc('text', usetex=False) 
        plt.rc('font', family='serif')
        
        plt.plot(it_tracker.iteration,
                 it_tracker.obj_fun,
                 label=arg2, color='black')

        plt.legend(frameon=False, loc=2, fontsize=10)
        plt.xlabel('Optimization Step')
        plt.ylabel('Objective f(p)')        
        plt.tight_layout()        
        plt.savefig(wd+'/jules_run/'+arg2+'.calibration_tracker.png', dpi=300)        
        plt.close()    
    
    return(obj_fun)

if f_minimize:
    
    #--------------------#
    #--- Optimization ---#
    #--------------------#
    
    #--- read initial calibration setup
    calib_setup = u.df_csv(wd+'/'+ini_calib_setup_fn)
    
    #--- filter only calibrate parameters
    calib_setup = calib_setup[:][calib_setup.calibrate]
    
    #--- initial parameters scaled
    p_ini = (calib_setup.ini - calib_setup.min_v) / (calib_setup.max_v - calib_setup.min_v)
    
    #--- initialize iteration tracker
    it_tracker = pd.DataFrame(columns=np.append(['iteration','obj_fun'],
                                                np.array(calib_setup.variable)))
    #--- write a brand new tracker file
    it_tracker.to_csv(wd+'/jules_run/'+arg2+'.calibration_tracker.csv', index = None, header=True)
    
    #--- write the calibration setup file
    calib_setup_fn = wd+'/jules_run/'+arg2+'.calibration_setup.csv'
    calib_setup.to_csv(calib_setup_fn, index = None, header=True)
    
    #--- Optimize parameters
    res = minimize(perf_dash, p_ini, method='nelder-mead',
                   options={'xatol': float('1e-'+str(prec_obj_fun)), 'disp': True})
    
    #--- Get results
    p_calib = res.x # debug p_calib = np.array([0.5,0.5])
    
    #--- read calibration setup
    calib_setup = u.df_csv(calib_setup_fn)
    
    #--- re-scale
    p_calib = np.array(calib_setup.min_v[calib_setup.calibrate] + (calib_setup.max_v[calib_setup.calibrate] - calib_setup.min_v[calib_setup.calibrate]) * p_calib).round(max(calib_setup.prec))
    
    #--- update in calibration setup
    calib_setup.loc[calib_setup['calibrate'], 'calib'] = p_calib
    
    #--- write results
    calib_setup.to_csv(calib_setup_fn, index = None, header=True)

if compare_res:
    
    #-----------------------#
    #--- compare results ---#
    #-----------------------#
    
    #--- get calib setup name
    calib_setup_fn = wd+'/jules_run/'+arg2+'.calibration_setup.csv'
    
    #--- read results from calibration setup
    calib_setup = u.df_csv(calib_setup_fn)

    #--- filter only calibrate parameters
    calib_setup = calib_setup[:][calib_setup.calibrate]

    #--- calibrated parameters scaled
    p_cal = (calib_setup.calib - calib_setup.min_v) / (calib_setup.max_v - calib_setup.min_v)
    
    #--- run comparison
    obj_fun = perf_dash(p_cal,
                        std_penalty = 1e6,
                        plot_tracker= False,
                        compare_res = compare_res)    

#--- track time
print("\nElapsed time of calibration "+str(arg2)+": --- %.3f seconds ---" % (time() - run_start))