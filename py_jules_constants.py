# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:58:20 2020

#--------------------------------------------------------------#
#------------------ py_jules_constants ------------------------# 
#--------------------------------------------------------------#
#--- Goal: 
#---    Declare all constants for py_jules simulations
#--- Author:
#---    Murilo Vianna (murilodsv@gmail.com)
#--------------------------------------------------------------#

"""

#---------------------------------#
#--- Constants to run py-jules ---#
#---------------------------------#

# *** Patch for Sugarcane and Sorghum: Both will be run as the Maize tile untill developed code is available

import pandas as pd

#--- Corresponding Crop ID number for pft arrays
#--- Following same order published before ['Wheat','Soybean','Maize','Rice'] Tab 3 of https://doi.org/10.5194/gmd-8-1139-2015
#--- Source: https://jules-lsm.github.io/latest/namelists/jules_surface_types.nml.html#JULES_SURFACE_TYPES::ncpft
id_crop_pft  = pd.DataFrame({'n_id'     : [6,7,8,9],                                       
                             'crop'     : ['Wheat','Soybean','Maize','Rice'],
                             'namelist' : ['jules_pftparm'] * 4})

#--- Corresponding Crop ID number for tile fractions order
#--- Following same order published before ['Wheat','Soybean','Maize','Rice'] Tab 3 of https://doi.org/10.5194/gmd-8-1139-2015
#--- Source: https://jules-lsm.github.io/latest/namelists/jules_surface_types.nml.html#JULES_SURFACE_TYPES::ncpft
n_tile_frac  = pd.DataFrame({'n_id'     : [1     ,     2,     3,     4,     5,      6,        7,      8,     9,     10,     11,     12,    13],                                       
                             'crop'     : ['pft1','pft2','pft3','pft4','pft5','Wheat','Soybean','Maize','Rice','pft10','pft11','pft12','pft13']})

#--- Corresponding Crop ID number for crop parameters arrays
#--- Following same order published before ['Wheat','Soybean','Maize','Rice'] Tab 3 of https://doi.org/10.5194/gmd-8-1139-2015
#--- Source: https://jules-lsm.github.io/latest/namelists/crop_params.nml.html
id_crop_par  = pd.DataFrame({'n_id'     : [1,2,3,4],
                             'crop'     : ['Wheat','Soybean','Maize','Rice'],
                             'namelist' : ['jules_cropparm'] * 4})

#--- Crop Codes
crop_codes   = pd.DataFrame({'crop_code': ['WT','SB','MZ','RC','SC','SG'],
                             'crop'     : ['Wheat','Soybean','Maize','Rice','Sugarcane','Sorghum']})

#--- Constant formats for jules driving data
fmt_driv_jules = pd.DataFrame({'val'    : [ 'sw_down', 'lw_down',  'precip',       't',    'wind',   'pstar',       'q', 'diff_rad'],
                               'fmt'    : ['{:16.2f}','{:16.2f}','{:12.4e}','{:16.2f}','{:16.2f}','{:16.1f}','{:16.8f}', '{:16.2f}']})

#--- Carbon to biomass conversion
#--- cfrac_r_io     = 0.439 [https://doi.org/10.5194/gmd-10-1291-2017]
#--- cfrac_l_io     = 0.439 [https://doi.org/10.5194/gmd-10-1291-2017]
#--- cfrac_s_io     = 0.439 [https://doi.org/10.5194/gmd-10-1291-2017]
#--- cropharvc      = 0.491 [Penning de Vries et al 1989, Tab 11]
#--- cropreservec   = 0.439 [assuming same as stem]
#--- leafC          = 0.400 [following sup material of Emma's paper for miscanthus: https://doi.org/10.5194/gmd-13-1123-2020] - claimed as hardcoded in JULES, so its better to use the same value here
#--- rootC          = 0.400 [following sup material of Emma's paper for miscanthus: https://doi.org/10.5194/gmd-13-1123-2020] - claimed as hardcoded in JULES, so its better to use the same value here
#--- woodC          = 0.480 [following sup material of Emma's paper for miscanthus: https://doi.org/10.5194/gmd-13-1123-2020] - claimed as hardcoded in JULES??, so its better to use the same value here
c_2_b = pd.DataFrame({'sim_code': ['croprootc' , 'cropstemc' , 'cropharvc' , 'cropreservec', 'cropleafc' , 'leafC', 'rootC', 'woodC'],
                      'conv_var': ['cfrac_r_io', 'cfrac_s_io',         None, 'cfrac_s_io'  , 'cfrac_l_io',    None,    None,    None],
                      'conv_ref': [       0.439,        0.439,        0.491,          0.439,        0.439,    0.40,    0.40,    0.48]})

#--- Grain Moisture Default Value used (13% for Maize)
#--- This will be used to convert cropharvc and cropyield to biomass
grain_h2o = 0.13

#--- Assuming 100% of harvest efficiency as default
#--- This is the efficiency related to the machinery/method used in the harvesting operation
#--- This will be used to convert cropharvc and cropyield to biomass
harv_eff  = 1.00

#--- Harvest Index of harvestable parts (yield_frac i.e. fraction of 'harvest' carbon pool that is grain rather than husk, cob etc)
#--- This default value is used when the paramter yield_frac is not available
#--- Using 0.74 following KW's paper: Tab3 (https://doi.org/10.5194/gmd-10-1291-2017)
yield_frac = 0.74

#--- Soil depth comparison deviation limit [m]
#--- This is used to match soil depth observations 'depth_m' with the mid point depth of each soil layer simulated
#--- If the difference abs(depth_m[layer] - mid[layer]) > d_dev_limit then observations will not be compared with simulations for that layer
d_dev_limit = 0.1 # 10 cm limit
 

