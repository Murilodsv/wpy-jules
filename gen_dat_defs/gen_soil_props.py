# -*- coding: utf-8 -*-
"""
#---> Created on Mon Feb 17 15:47:31 2020

Goal: Generate the soil data of site-specific for JULES simulations

@author: Murilo Vianna (murilodsv@gmail.com)
"""

def gen_soil_props(setup_fn:str,
                   out_fn = None,
                   ml     = False):

    #---------------------------------------------------------------#
    #------------------------ gen_soil_props -----------------------# 
    #---------------------------------------------------------------#
    #--- Goal: 
    #---    Generate the soil data of site-specific for JULES simulations.
    #--- Parameters: 
    #---    setup_fn   : Input .CSV file
    #---    out_fn     : Output filename                       [optional]
    #---    ml         : Flag for multiple soil layers
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    #--- Load Global Packages
    import pandas as pd
    import os
    import datetime
    from time import gmtime, strftime, time
    
    #--- Load internal Packages
    import gen_nml_defs as gd
    
    #--- Track progress
    start_time = time()
    warn_msg   = ['Warning Logs for Namelist creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    erro_msg   = ['Error Logs for Namelist creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    
    if out_fn == None:
        out_fn   = setup_fn.replace('.csv','.txt')
        
    if not '.csv' in setup_fn:    
        import sys        
        #--- Only CSV files accepted for now
        msg = "Error: The template setup file must be an .csv file."
        print(msg+'\nSoil data not created.')
        erro_msg.append(msg)            
        sys.exit(1)
    
    #--- Soil Layer Template (hardwired)
    soil_layer_temp = '<b> <hcap> <sm_wilt> <hcon> <sm_crit> <satcon> <sathh> <sm_sat> <albsoil>'
    
    #--- Default values in case some variable is missing
    default_soil = pd.DataFrame({'temp_var' : ['<b>','<hcap>','<sm_wilt>', '<hcon>', '<sm_crit>', '<satcon>', '<sathh>', '<sm_sat>', '<albsoil>'],
                                 'val'      : ['8.408', '1.156E+06', '0.2488', '0.2055', '0.3917', '0.00144', '0.6278', '0.4782', '0.133']})
    
    #--- Run info
    time_now = datetime.datetime.now()
    sim_id   = out_fn.split('/')[-1]
    
    #--- Open csv as DataFrame with variables setup
    var_setup = pd.DataFrame(pd.read_csv(setup_fn))
    
    #--- Convert NaNs to ''
    var_setup = var_setup.fillna('')
    
    #--- Initiate soil file
    soil_file_arr = []
    soil_file_arr.append('# Soil characteristics for:        '+sim_id)
    soil_file_arr.append('# Source .CSV file used:           '+setup_fn)
    soil_file_arr.append('# Created by gen_soil_props.py at: '+str(time_now))
    soil_file_arr.append('# b   hcap   sm_wilt   hcon  sm_crit  satcon sathh  sm_sat  albsoil')
    
    #--- Initialize template    
    if ml:
        rep_temp = ' '.join(list(var_setup['temp_var']))
    else:    
        rep_temp = soil_layer_temp
    
    #--- Replace for every soil parameter
    for f in var_setup['temp_var']:
        if f in rep_temp:
            
            #--- Parameter info
            var     = var_setup['val' ][var_setup['temp_var'] == f].values[0]
            t_var   = var_setup['type'][var_setup['temp_var'] == f].values[0]
            p_var   = var_setup['prec'][var_setup['temp_var'] == f].values[0]
            
            #--- Format parameter for replacing
            rep     = gd.format_var(var,t_var,p_var)
            
            #--- Replace into template layer
            rep_temp = rep_temp.replace(f,rep)
            
        else:
            
            #--- This variable was not found on soil layer template
            msg = "Warning: Parameter '"+f+"' not found on soil layer template.\nParameters accepted are: "+soil_layer_temp
            print(msg)
            warn_msg.append(msg)
    
    #--- Check if any soil info was missing
    if '<' in rep_temp:
        
        #--- add from default
        for f in default_soil['temp_var']:
            if f in rep_temp:
                
                #--- Parameter info
                var     = default_soil['val' ][default_soil['temp_var'] == f].values[0]
                t_var   = 'real'
                p_var   = 4
                
                #--- Format parameter for replacing
                rep     = gd.format_var(var,t_var,p_var)
                
                #--- Replace into template layer
                rep_temp = rep_temp.replace(f,rep)
                
                msg = "Warning: Soil parameter '"+f+"' not found in file '"+setup_fn+"'.\nDefault value of '"+var+"' was set for '"+f+"'"
                print(msg)
                warn_msg.append(msg)
    
    #--- Append to soil file
    soil_file_arr.append(rep_temp)
    
    #--- Write file
    with open(out_fn, 'w') as f:
            for item in soil_file_arr:
                f.write("%s\n" % item)
    
    #--- Check progression
    if len(warn_msg) > 1:
        
        #--- Warnings found
        print("Soil properties file '"+out_fn+"' created but some warnings were generated and can be found at file: 'warnings_soil_prop.wng'")
        with open('warnings_soil_prop.wng', 'w') as f:
            for item in warn_msg:
                f.write("%s\n" % item)
                
    else:
        
        #--- No Warnings
        print("Soil properties file '"+out_fn+"' created succesfully at 'data/'")
        if os.path.exists('warnings_soil_prop.wng'):
            os.remove('warnings_soil_prop.wng')
        
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))


