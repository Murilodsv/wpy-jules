# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:56:27 2020

@author: muril
"""

def get_grain_h20(run_id,
                  dash_run):
    
    #--- try to get grain_h2o from dashboard
    try:
        grain_h2o  = float(dash_run['grain_moisture'][dash_run['run_id'] == run_id].values[0])
        
        #--- check for nan
        if grain_h2o != grain_h2o: raise ValueError('Error: grain_h2o read as nan')    
                            
        if grain_h2o < 0 or grain_h2o >= 1:
            import py_jules_constants as c
            grain_h2o  = c.grain_h2o
            print('Warning: The value of grain_moisture from dashboard file for run_id: '+str(run_id)+' is out of bounds 0-1.\n --- The default value of '+str(grain_h2o)+' was assumed --- ')                    
    except:
        import py_jules_constants as c
        grain_h2o  = c.grain_h2o
        print('Warning: Could not retrieve a float value for grain_moisture from dashboard file for run_id: '+str(run_id)+'.\n --- The default value of '+str(grain_h2o)+' was assumed --- ')
        
    return(grain_h2o)