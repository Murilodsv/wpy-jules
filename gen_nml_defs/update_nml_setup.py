# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:37:06 2020

@author: muril
"""

def update_nml_setup(base_nml_fn:str,
                     driv_meta_fn = None,
                     soil_meta_fn = None,
                     crop_meta_fn = None,
                     mana_meta_fn = None,
                     base_out_fn  = None):

    #--------------------------------------------------------------#
    #---------------------- update_nml_setup ----------------------# 
    #--------------------------------------------------------------#
    #--- Goal: 
    #---    Update base setup namelist file for jules simulations
    #--- Parameters: 
    #---    base_nml_fn     : Filename for the base setup CSV file
    #---    driv_meta_fn    : Filename for drive meta info to be updated
    #---    soil_meta_fn    : Filename for soil meta info to be updated
    #---    crop_meta_fn    : Filename for crop meta info to be updated
    #---    mana_meta_fn    : Filename for managements (also any ancillaries) meta info to be updated
    #---    base_out_fn     : Output Filename (CSV)
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    #--- Load Global Packages
    import pandas as pd
    
    #--- Matching columns
    cols = ['variable','file','namelist','array_id','n_nl']
    
    #--- Open base info nml
    base_nml = pd.DataFrame(pd.read_csv(base_nml_fn))
    
    #--- Generate combined id
    base_nml['combined'] = base_nml[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
    
    #--- Merge meta input
    l_meta = [driv_meta_fn,
              soil_meta_fn,
              crop_meta_fn,
              mana_meta_fn]
    
    #--- Loop over meta info
    for meta in l_meta:
        
        if not meta == None:
            
            #-------------------#
            #--- Update info ---#
            #-------------------#
            
            #--- Open meta data
            meta_data = pd.DataFrame(pd.read_csv(meta))
            
            #--- Generate combined id
            meta_data['combined'] = meta_data[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
            
            #--- Drop matching variables of info
            base_nml = base_nml[:][~base_nml['combined'].isin(meta_data['combined'])]
            
            #--- Append meta to base nml
            base_nml = base_nml.append(meta_data)              
    
    #--- Drop combined indexers
    del base_nml['combined']
    
    #--- write updated setup_nml    
    if base_out_fn == None:
        base_out_fn = base_nml_fn.replace('.csv','_update.csv')   
    
    base_nml.to_csv(base_out_fn, index = None, header=True)
                        