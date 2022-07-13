# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:40:40 2020

@author: muril
"""

def c2b_frac(vn,
             run_id,
             setup_nml):
    
    import py_jules_constants as c
        
    if vn in c.c_2_b['sim_code'].values:
        
        #--- conv_var
        conv_var = c.c_2_b['conv_var'][c.c_2_b['sim_code'].values == vn].values[0]
        
        if type(conv_var) == type(None):
            #--- Use default values declared in py_jules_constants.py
            cfrac = float(c.c_2_b['conv_ref'][c.c_2_b['sim_code'].values == vn].values[0])
            print('Warning: Converting '+str(vn)+' from carbon to biomass using default value in py_jules_constants.py = '+str(cfrac))
        else:
            #--- Look-up in nml parameters                                        
            f = setup_nml['variable'] == c.c_2_b['conv_var'][c.c_2_b['sim_code'].values == vn].values[0]
        
            #--- crop code
            c_code = run_id[0:2]
            
            #--- if sugarcane or sorghum convert to maize
            # *** PATCH for Sugarcane and Sorghum
            if c_code == 'SC' or c_code == 'SG': c_code = 'MZ'
            
            #--- get crop name
            c_nm = c.crop_codes['crop'][c.crop_codes['crop_code'] == c_code].values[0]
                                                
            #--- find in nml the parameters fractions of C in B
            cfrac_nml = setup_nml[['val','array_id']][f]
            f_crop    = c.id_crop_par['n_id'][c.id_crop_par['crop'] ==c_nm].values[0]
            
            #--- get the corresponding cpft one
            cfrac = float(cfrac_nml['val'][cfrac_nml['array_id'] == f_crop].values[0])                                                    
        
    else:
        print('Warning: No conversion factor found to convert Carbon to Biomass for variable '+str(vn)+'.\n --- A value of 0.5 is assumed ---')
        cfrac = 0.5
    
    #--- return
    return(cfrac)