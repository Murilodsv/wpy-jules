# -*- coding: utf-8 -*-
"""
Created on Thu May 14 20:33:07 2020

@author: muril
"""

def merge_soil_data_by_layer(obs_df,
                             sim_df,
                             merge_idx):    

    import pandas as pd    
            
    if 'depth_m' in obs_df.keys(): 
                                                                            
        l_id = 1
        sim_df['layer_id'] = 0
        obs_df['layer_id'] = 0
                     
        for d_obs in obs_df['depth_m'].unique():
            
            #--- soil discretization
            soil_disc = sim_df[['bot','top','mid']].drop_duplicates()
            
            #--- position of matched layer
            f = (d_obs <= soil_disc['bot']) & (d_obs > soil_disc['top'])
                        
            #--- get the best match with depth
            d_sim = soil_disc['mid'][f].values[0]
            
            #--- add layer_id
            if any(sim_df.loc[sim_df['mid']     == d_sim,'layer_id'] > 0):
                
                print('Warning: More than one soil layer observation set of values falls within the same simulated soil layer:')
                print(str(round(soil_disc['top'][f].values[0],2)) + ' < '+str(d_obs)+' >= '+str(round(soil_disc['bot'][f].values[0],2)))
                obs_df.loc[obs_df['depth_m'] == d_obs,'layer_id'] = l_id - 1
            else:
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
    
