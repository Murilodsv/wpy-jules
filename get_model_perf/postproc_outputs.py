# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:08:48 2020

@author: muril
"""

def postproc_outputs(v,
                     res,
                     dash_run,
                     setup_nml,
                     run_id,
                     time_idx):
    
    from get_model_perf import get_biomass_vars    
    
    #------------------------#
    #--- Stalk Dry Weight ---#
    #------------------------#
    if v == 'stalk_dw':        
        
        #--- list of JULES-crop' dependent variables
        l_vars = ['cropstemc', 'cropreservec']        
        
        #--- get variables already converting C to Biomass
        df = get_biomass_vars(v,
                              l_vars,
                              res,
                              run_id,
                              setup_nml,
                              time_idx)
        
        if type(df) == type(None):
            
            #--- Variable not found for JULES-crop, try to get for JULES pfts
            print('Warning: JULES-Crop output not found to compute the observed variable '+v+', instead postproc_outputs.py will try to compute it using JULES pft outputs.')            
            
            #--- Correspondent pft variable
            l_vars = ['woodC']
            
            #--- get variables already converting C to Biomass
            df = get_biomass_vars(v,
                                  l_vars,
                                  res,
                                  run_id,
                                  setup_nml,
                                  time_idx)
            
            if type(df) != type(None):                        
                #--- generate corresponding columns
                df['cropstemc']     = df['woodC']
                df['cropreservec']  = 0. # there's no distinction between reserves/stems parts using pfts
        
        if type(df) != type(None):            
                        
            #--- Compute stalk_dw in ton ha-1
            df['sim_value'] = (df['cropstemc'] + df['cropreservec']) * 10.
            df['sim_code']  = v
            
            #--- result df
            df = df[time_idx+['sim_value','sim_code']]
            
    #-------------------------#
    #--- Sugars Dry Weight ---#
    #-------------------------#
    elif v == 'sugars_dw':
        
        #--- list of JULES-crop' dependent variables
        l_vars = ['cropreservec']
        
        #--- get variables already converting C to Biomass
        df = get_biomass_vars(v,
                              l_vars,
                              res,
                              run_id,
                              setup_nml,
                              time_idx)
        
        if type(df) != type(None):            
                        
            #--- Compute sugars_dw in ton ha-1
            df['sim_value'] = df['cropreservec'] * 10.
            df['sim_code']  = v
            
            #--- result df
            df = df[time_idx+['sim_value','sim_code']]    
            
    #------------------------------#
    #--- Harvestable Dry Weight ---#
    #------------------------------#
    elif v == 'harv_dw':
        
        #--- list of JULES-crop' dependent variables
        l_vars = ['cropharvc']
        
        #--- get variables already converting C to Biomass
        df = get_biomass_vars(v,
                              l_vars,
                              res,
                              run_id,
                              setup_nml,
                              time_idx)
        
        if type(df) == type(None):
            
            #--- Variable not found for JULES-crop, try to get for JULES pfts
            print('Warning: JULES-Crop output not found to compute the observed variable '+v+', instead postproc_outputs.py will try to compute it using JULES pft outputs.')            
            
            #--- Correspondent pft variable
            l_vars = ['harvest']
            
            #--- get variables already converting C to Biomass
            df = get_biomass_vars(v,
                                  l_vars,
                                  res,
                                  run_id,
                                  setup_nml,
                                  time_idx)
            
            if type(df) != type(None):            
                #--- generate corresponding columns
                df['cropharvc']     = df['harvest']            
        
        if type(df) != type(None):            
                        
            #--- Compute harv_dw in ton ha-1
            df['sim_value'] = df['cropharvc'] * 10.
            df['sim_code']  = v
            
            #--- result df
            df = df[time_idx+['sim_value','sim_code']]
    
    #------------------------#
    #--- Grain Dry Weight ---#
    #------------------------#
    #--- In this case, dry weight is corrected using:
    #---    Harvest index [JULES-Crop namelist]
    #---    Grain Moisture [dashboard]
    #---    Harvest Efficiency [dashboard]
    elif v == 'grain_dw':
        
        from get_model_perf import get_yield_frac
        from get_model_perf import get_grain_h20
        from get_model_perf import get_harv_eff
        
        #--- list of JULES-crop' dependent variables
        l_vars = ['cropharvc']
        
        #--- get variables already converting C to Biomass
        df = get_biomass_vars(v,
                              l_vars,
                              res,
                              run_id,
                              setup_nml,
                              time_idx)
        
        if type(df) == type(None):
            
            #--- Variable not found for JULES-crop, try to get for JULES pfts
            print('Warning: JULES-Crop output not found to compute the observed variable '+v+', instead postproc_outputs.py will try to compute it using JULES pft outputs.')            
            
            #--- Correspondent pft variable
            l_vars = ['harvest']
            
            #--- get variables already converting C to Biomass
            df = get_biomass_vars(v,
                                  l_vars,
                                  res,
                                  run_id,
                                  setup_nml,
                                  time_idx)
            
            if type(df) != type(None):
                #--- generate corresponding columns
                df['cropharvc']     = df['harvest']
        
        if type(df) != type(None):
            
            #--- Compute harv_dw in ton ha-1
            df['sim_value'] = df['cropharvc'] * 10.
            df['sim_code']  = v
            
            #--- Get yield_frac from nml
            yield_frac = get_yield_frac(run_id,
                                        setup_nml)
            
            #--- Get Grain Moisture from dashboard            
            grain_h2o = get_grain_h20(run_id,
                                      dash_run)
            
            #--- Get Harvesting Efficiency from dashboard
            harv_eff =  get_harv_eff(run_id,
                                     dash_run)
            
            #--- Convert harvastable dw to grain_dw [ton ha-1]            
            df['sim_value'] = df['sim_value'] * harv_eff * yield_frac / (1-grain_h2o)
            
            #--- result df
            df = df[time_idx+['sim_value','sim_code']]
            
    #-----------------------#
    #--- Leaf Dry Weight ---#
    #-----------------------#
    elif v == 'leaf_dw':
        
        #--- list of JULES-crop' dependent variables
        l_vars = ['cropleafc']
        
        #--- get variables already converting C to Biomass
        df = get_biomass_vars(v,
                              l_vars,
                              res,
                              run_id,
                              setup_nml,
                              time_idx)
        
        if type(df) == type(None):
            
            #--- Variable not found for JULES-crop, try to get for JULES pfts
            print('Warning: JULES-Crop output not found to compute the observed variable '+v+', instead postproc_outputs.py will try to compute it using JULES pft outputs.')            
            
            #--- Correspondent pft variable
            l_vars = ['leafC']
            
            #--- get variables already converting C to Biomass
            df = get_biomass_vars(v,
                                  l_vars,
                                  res,
                                  run_id,
                                  setup_nml,
                                  time_idx)
            
            if type(df) != type(None):
                #--- generate corresponding columns
                df['cropleafc']     = df['leafC']            
        
        if type(df) != type(None):
                        
            #--- Compute leaf_dw in ton ha-1
            df['sim_value'] = df['cropleafc'] * 10.
            df['sim_code']  = v
            
            #--- result df
            df = df[time_idx+['sim_value','sim_code']]
            
    #------------------------#
    #--- Roots Dry Weight ---#
    #------------------------#
    elif v == 'root_dw':
        
        #--- list of JULES-crop' dependent variables
        l_vars = ['croprootc']
        
        #--- get variables already converting C to Biomass
        df = get_biomass_vars(v,
                              l_vars,
                              res,
                              run_id,
                              setup_nml,
                              time_idx)

        if type(df) == type(None):
            
            #--- Variable not found for JULES-crop, try to get for JULES pfts
            print('Warning: JULES-Crop output not found to compute the observed variable '+v+', instead postproc_outputs.py will try to compute it using JULES pft outputs.')            
            
            #--- Correspondent pft variable
            l_vars = ['rootC']
            
            #--- get variables already converting C to Biomass
            df = get_biomass_vars(v,
                                  l_vars,
                                  res,
                                  run_id,
                                  setup_nml,
                                  time_idx)
            
            if type(df) != type(None):            
                #--- generate corresponding columns
                df['croprootc']     = df['rootC']
            
        if type(df) != type(None):            
                        
            #--- Compute root_dw in ton ha-1
            df['sim_value'] = df['croprootc'] * 10.
            df['sim_code']  = v
            
            #--- result df
            df = df[time_idx+['sim_value','sim_code']]
    
    #-------------------------#
    #--- Aerial Dry Weight ---#
    #-------------------------#        
    elif v == 'aerial_dw':
        
        #--- list of JULES-crop' dependent variables
        l_vars = ['cropstemc', 'cropreservec','cropleafc','cropharvc']
        
        #--- get variables already converting C to Biomass
        df = get_biomass_vars(v,
                              l_vars,
                              res,
                              run_id,
                              setup_nml,
                              time_idx)
        
        if type(df) == type(None):
            
            #--- Variable not found for JULES-crop, try to get for JULES pfts
            print('Warning: JULES-Crop output not found to compute the observed variable '+v+', instead postproc_outputs.py will try to compute it using JULES pft outputs.')            
            
            #--- Correspondent pft variable
            l_vars = ['leafC', 'woodC']
            
            #--- get variables already converting C to Biomass
            df = get_biomass_vars(v,
                                  l_vars,
                                  res,
                                  run_id,
                                  setup_nml,
                                  time_idx)
            
            if type(df) != type(None):
                #--- generate corresponding columns
                df['cropstemc']     = df['woodC']            
                df['cropleafc']     = df['leafC']
                df['cropharvc']     = 0.
                df['cropreservec']  = 0.                
        
        if type(df) != type(None):      
                        
            #--- Compute aerial_dw in ton ha-1
            df['sim_value'] = (df['cropstemc'] + df['cropreservec'] + df['cropleafc'] + df['cropharvc']) * 10.
            df['sim_code']  = v
            
            #--- result df
            df = df[time_idx+['sim_value','sim_code']]

    #-----------#
    #--- LAI ---#
    #-----------#        
    elif v == 'croplai':
        
        from get_model_perf import find_var_res
        
        #--- Get crop lai [m2 m-2]
        df = find_var_res('croplai',res,time_idx)
        
        if type(df) == type(None):
            
            #--- Variable not found for JULES-crop, try to get for JULES pfts
            print('Warning: JULES-Crop output not found to compute the observed variable '+v+', instead postproc_outputs.py will try to compute it using JULES pft outputs.')            
            
            #--- Get pft lai [m2 m-2]
            df = find_var_res('lai',res,time_idx)
        
        if type(df) != type(None):            
                        
            #--- LAI doesn't need convertion
            df['sim_value'] = df['sim_value'] * 1.
            df['sim_code']  = v
            
    #--------------------#
    #--- Stalk height ---#
    #--------------------#        
    elif v == 'cropcanht':
        
        from get_model_perf import find_var_res
        
        #--- Get crop height [m]
        df = find_var_res('cropcanht',res,time_idx)
        
        if type(df) == type(None):
            
            #--- Variable not found for JULES-crop, try to get for JULES pfts
            print('Warning: JULES-Crop output not found to compute the observed variable '+v+', instead postproc_outputs.py will try to compute it using JULES pft outputs.')            
            
            #--- Get pft height [m]
            df = find_var_res('canht',res,time_idx)
        
        if type(df) != type(None):            
                        
            #--- Canopy height doesn't need convertion [m]
            df['sim_value'] = df['sim_value'] * 1.
            df['sim_code']  = v            

    #--------------------------#
    #--- Evapotranspiration ---#
    #--------------------------#        
    elif v == 'et':
        
        from get_model_perf import find_var_res
        
        #--- Get tile surface moisture flux for land tiles (kg m-2 s-1)
        df = find_var_res('fqw',res,time_idx)
        
        if type(df) != type(None):            
                        
            #--- Compute ET in mm day-1
            df['sim_value'] = df['sim_value'] * 86400.           
            df['sim_code']  = v
            
    #---------------------#
    #--- Soil Moisture ---#
    #---------------------#        
    elif v == 'swc':
        
        from get_model_perf import get_l_var
        import pandas as pd
        
        #--- Dependent variables
        l_vars = ['soil_wet','sm_sat']
        
        #--- Get soil moisture from JULES' outputs [kg m-2]
        df = get_l_var(v,
              l_vars,
              res,
              run_id,
              setup_nml,
              time_idx+['soil'])
        
        if type(df) != type(None):            
                        
            #--- Compute soil compartments
            df_depth = setup_nml[['array_id','val']][setup_nml['variable'] == 'dzsoil_io']
            df_depth['size'] = df_depth['val'].astype(float).values
            
            #--- sort by array_id
            df_depth = df_depth.sort_values(by=['array_id']).reset_index(drop = True)
            
            #--- sizes
            df_depth['top'] = 0
            df_depth['bot'] = 0
            df_depth['dep'] = 0
            
            #--- top point
            for i in df_depth.index:
                if i == 0:
                    df_depth.loc[i,'dep'] = df_depth.loc[i,'size']                    
                else:
                    df_depth.loc[i,'dep'] = df_depth.loc[i-1,'dep'] + df_depth.loc[i,'size']                    
                    df_depth.loc[i,'top'] = df_depth.loc[i-1,'dep']
                        
            df_depth['bot'] = df_depth['dep']
                            
            #--- mid point
            df_depth['mid'] = (df_depth['top'] + df_depth['bot']) / 2
                                    
            #--- merge with data
            df = pd.merge(df, df_depth, left_on='soil', right_on='array_id')
                        
            #--- compute SWC in m3/m3
            #--- sm_sat [m3/m3] and soil_wet [0-1]
            df['sim_value'] = df['soil_wet'] * df['sm_sat']
            df['sim_code']  = v
        
    else:
        print('Warning: Variable '+v+' not found in the postproc_outputs.py list so it will not be computed.')
        df = None
    
    if type(df) != type(None): 
        print('Variable '+str(v)+' computed by postproc_outputs.py')
    
    return(df)