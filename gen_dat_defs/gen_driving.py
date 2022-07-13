# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:31:09 2020

Goal: Generate the driving data of site-specific for JULES simulations

@author: Murilo Vianna (murilodsv@gmail.com)
"""

def gen_driving(driv_nm:str,
                datetime_ini    = None,
                dt              = None,
                l_driv_data     = None,
                l_driv_fmt      = None,
                out_fn          = None):
    
    #--------------------------------------------------------------#
    #------------------------ gen_driving -------------------------# 
    #--------------------------------------------------------------#
    #--- Goal: 
    #---    Converts driving data from csv format to JULESs format.
    #--- Parameters: 
    #---    driv_nm         : CSV filename of input driving data           
    #---    datetime_ini    : Initial date and time of the input driving data (YYYY-MM-DD HH:MM:SS)     [optional]
    #---    dt              : Timestep of the input driving data                                        [optional]
    #---    l_driv_data     : List of variables and order to be arranged in output                      [optional]
    #---    l_driv_fmt      : Format of variables provided in -ldata (e.g. {:16.2f})                    [optional]
    #---    out_fn          : Output filename for driving data                                          [optional]
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    import pandas as pd
    import os
    from time import gmtime, strftime, time

    #--- Track progress
    start_time = time()
    
    #--- Logs Warning and Errors
    warn_msg   = ['Warning Logs for driving creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    erro_msg   = ['Error Logs for driving creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    
    #--- Check arguments
    if not '.csv' in driv_nm:
        
        import sys
        
        #--- Only CSV files accepted for now
        msg = "Error: The template setup file must be an .csv file."
        print(msg+'\nDriving data not created.')
        erro_msg.append(msg)            
        sys.exit(1)
        
    if out_fn == None:
        out_fn = driv_nm.replace(".csv",".dat")
    
    #--- Open csv as DataFrame
    driv_df = pd.DataFrame(pd.read_csv(driv_nm))
    
    #--- check list arguments
    if l_driv_data == None:
        l_driv_data = list(driv_df.keys())
        msg = "Warning: List of driving data not provided, using all variables found in input file:\n"+" ".join(l_driv_data)
        print(msg)
        warn_msg.append(msg)
        
    if l_driv_fmt == None:
       l_driv_fmt = ['{:16.2f}'] * len(l_driv_data)
       msg = "Warning: List of formats for driving data is not provided, using default values:\n"+" ".join(l_driv_fmt)
       print(msg)
       warn_msg.append(msg)
    
    if len(l_driv_fmt) != len(l_driv_data):
            
        #--- different variable and format lengths
        if len(l_driv_fmt) > len(l_driv_data):
            l_driv_fmt = l_driv_fmt[0:(len(l_driv_data)-1)]
        else:
            for i in (len(l_driv_data) - len(l_driv_fmt)):
                l_driv_data.append('{:16.2f}')
    
        msg = "Warning: Different lenghts of variables and formats. Missing formats assumed as default (:16.2f)."
        print(msg)
        warn_msg.append(msg)            
        
    #--- Initialize drive file
    out =        ['# Created by gen_driving.py at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'\n',
                  '# Input csv file:        '+driv_nm+'\n',
                  '# First date:            '+str(datetime_ini)+'\n',
                  '# Timestep in seconds:   '+str(dt)+'\n',
                  '# sw_down lw_down precip  t wind  pstar q diff_rad'+'\n',
                  '# Wm-2 Wm-2 kgm-2s-1 K ms-1 Pa kgkg-1 Wm-2'+'\n']
    
    #--- format numbers
    for i in range(len(l_driv_data)):
        driv_df[l_driv_data[i]] = driv_df[l_driv_data[i]].map(l_driv_fmt[i].format)
    
    #--- write as string
    out.append(driv_df[l_driv_data].to_string(justify='left', index=False, header=False))
    
    #--- write on file
    with open(out_fn, 'w') as f:
            for item in out:
                f.write("%s" % item)
                
    #--- Check progression
    if len(warn_msg) > 1:
        
        #--- Warnings found
        print("Drive file '"+out_fn+"' created but some warnings were generated and can be found at file: 'warnings_drive.wng'")
        with open('warnings_drive.wng', 'w') as f:
            for item in warn_msg:
                f.write("%s\n" % item)
                
    else:
        
        #--- No Warnings
        print("Drive file '"+out_fn+"' created succesfully at 'data/'")
        if os.path.exists('warnings_drive.wng'):
            os.remove('warnings_drive.wng')
        
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))
