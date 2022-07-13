# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:58:27 2020

@author: muril
"""

def get_harv_eff(run_id,
                  dash_run):
    
    #--- try to get harv_eff from dashboard
    try:
        harv_eff  = float(dash_run['harv_efficiency'][dash_run['run_id'] == run_id].values[0])
        
        #--- check for nan
        if harv_eff != harv_eff: raise ValueError('Error: harv_eff read as nan')            
        
        if harv_eff < 0 or harv_eff > 1:
            import py_jules_constants as c
            harv_eff  = c.harv_eff
            print('Warning: The value of harv_efficiency from dashboard file for run_id: '+str(run_id)+' is out of bounds 0-1.\n --- The default value of '+str(harv_eff)+' was assumed --- ')                
    except:
        import py_jules_constants as c
        harv_eff  = c.harv_eff
        print('Warning: Could not retrieve a float value for harv_efficiency from dashboard file for run_id: '+str(run_id)+'.\n --- The default value of '+str(harv_eff)+' was assumed --- ')
        
    return(harv_eff)