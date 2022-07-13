# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:15:13 2020

@author: muril
"""

def get_yield_frac(run_id,
                   setup_nml):
    
    import py_jules_constants as c
    
    #--- crop code
    c_code = run_id[0:2]
    
    #--- if sugarcane or sorghum convert to maize
    # *** PATCH for Sugarcane and Sorghum
    if c_code == 'SC' or c_code == 'SG': c_code = 'MZ'
    
    #--- get crop name
    c_nm = c.crop_codes['crop'][c.crop_codes['crop_code'] == c_code].values[0]
    
    #--- get crop cpft array
    arr_id = c.id_crop_par['n_id'][c.id_crop_par['crop'] == c_nm].values[0]
        
    #--- Look-up 'yield_frac' in the corresponding array of nml
    f = (setup_nml['variable'] == 'yield_frac_io') & (setup_nml['array_id'] == arr_id)
    
    #--- get yield frac from nml
    try:
        yield_frac = float(setup_nml['val'][f].values[0])
    except:
        yield_frac = c.yield_frac
        print('Warning: Could not retrieve yield_frac_io from nml file.\n --- The default value of '+str(yield_frac)+' is assumed ---')
        
    return(yield_frac)
