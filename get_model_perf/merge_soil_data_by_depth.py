# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 19:50:24 2020

@author: muril
"""


def merge_soil_data_by_depth(obs_df,
                             sim_df,
                             merge_idx):    

    import pandas as pd
    import py_jules_constants as c
            
    if 'depth_m' in obs_df.keys(): 
                                                                            
        l_id = 1
        sim_df['layer_id'] = 0
        obs_df['layer_id'] = 0
                     
        for d_obs in obs_df['depth_m'].unique():
            
            #--- absolute difference
            adif = abs(d_obs - sim_df['mid'].unique())                            
            
            # skip if depth difference is too high
            if min(adif) > c.d_dev_limit: continue 
            
            #--- position of best match
            f = adif == min(adif)
            
            #--- get the best match with depth
            d_sim = sim_df['mid'].unique()[f][0]
            
            #--- add layer_id
            sim_df.loc[sim_df['mid']     == d_sim,'layer_id'] = l_id
            obs_df.loc[obs_df['depth_m'] == d_obs,'layer_id'] = l_id
            
            l_id += 1
        
        #--- clean zeros
        sim_df     = sim_df[:][sim_df['layer_id'] != 0]
        obs_df     = obs_df[:][obs_df['layer_id'] != 0]
    
        #--- Merge simulated and observed data
        sim_obs_df = pd.merge(obs_df,sim_df, how = 'left', on = merge_idx+['layer_id'], suffixes=('_obs', '_sim'))
        
        #--- Gather results
        res = {'merged': sim_obs_df,
               'sim'   : sim_df,
               'obs'   : obs_df}        
    else:
        print('Warning: There is no column "depth_m" in observed soil data to compare with corresponding simulated soil layers.\n --- Observed soil data ignored --- ')
        res = None
        
    return(res)
    