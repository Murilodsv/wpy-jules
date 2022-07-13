# -*- coding: utf-8 -*-
"""
Created on Wed May  6 20:58:12 2020

@author: muril
"""

def get_conv_unitf(v,
                   meta):
    
    #--- Convert units to the same of observations
    u_meta = meta[['JULES_sim_code','JULES_unit_fac','units']]
    u_meta = u_meta[['units','JULES_unit_fac']][u_meta['JULES_sim_code'] == v]
    len_u  = len(u_meta.drop_duplicates())
    
    if len_u == 0:
        print('Warning: No conversion factor found in meta file for converting simulated results of "'+v+'" to the same units of observations.\n - A value of 1 will be assumed.')
        conv_factor = 1
        unit_lab    = None 
    elif len_u > 1:
        print('Warning: More than one conversion factor found in meta file for converting simulated results of "'+v+'" to the same units of observations.\n - Only the first ocurrence will be assumed.')
        conv_factor = u_meta['JULES_unit_fac'].values[0]
        unit_lab    = u_meta['units'].values[0]
    else:
        conv_factor = u_meta['JULES_unit_fac'].values[0]
        unit_lab    = u_meta['units'].values[0]
    
    return({'conv_factor': conv_factor,
            'unit_lab'   : unit_lab})
