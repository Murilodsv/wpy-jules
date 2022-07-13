# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 13:05:20 2020

@author: muril
"""

def gen_harv_doy(tf:float,
                  out_fn = 'harvest_doy.txt'):
    
    #--------------------------------------------------------------#
    #------------------------ gen_harv_doy ------------------------# 
    #--------------------------------------------------------------#
    #--- Goal: 
    #---    Generate the harvest doy file for JULES-BE TRIFFID simulations
    #--- Parameters: 
    #---    it         : List of ahrvest doy
    #---    out_fn     : Output filename                       [optional]
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------#

    from time import gmtime, strftime, time
    
    #--- Track progression
    start_time = time()
    
    #--- Initialize
    out =        ['# Created by gen_harv_doy.py at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'\n',
                  '# Harvest DOY'+'\n',
                  '# T1     T2     T3     T4     T5     WHEAT  SOYBE  MAIZE  RICE'+'\n']

    #--- Check inputs
    if out_fn == None:
        out_fn = 'harvest_doy.txt'
        
    if len(tf) > 9:
        msg   = 'More than 9 harvest doys provided.\n -- The only first 9 will be used.'
        print(msg)
    
    if len(tf) < 9:
        tf = tf + [0]*(9 - len(tf))
        msg   = 'Less than 9 harvest doys provided.\n -- First value set for missing tiles.'    
        print(msg)
    
    if any(i > 366 for i in tf) or any(i < 1 for i in tf):
        #--- Logs Warning and Errors
        import sys
        
        msg   = 'ERROR: One or more harvest doys provided is out of range (1-366).\n -- Please provide values between 1 and 366.\n -- Harvest doy file NOT CREATED.'
        print(msg)
        sys.exit(1)
    
    #--- Append to output
    out.append('  '+'    '.join(["{0:0.0f}".format(i) for i in tf]))
    
    #--- write on file
    with open(out_fn, 'w') as f:
            for item in out:
                f.write("%s" % item)
                
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))