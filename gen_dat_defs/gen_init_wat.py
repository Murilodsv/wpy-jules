# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:01:27 2020

Goal: Generate the initial soil moisture file for JULES-Crop simulations

@author: Murilo Vianna (murilodsv@gmail.com)
"""

def gen_init_wat(iw:float,
             out_fn = 'init_soil_moisture.dat'):    
    
    #---------------------------------------------------------------#
    #------------------------ gen_init_wat -------------------------# 
    #---------------------------------------------------------------#
    #--- Goal: 
    #---    Generate the initial soil moisture file for JULES-Crop simulations.
    #--- Parameters: 
    #---    iw         : List of initial soil moisture as fraction of saturation point (sm_sat).
    #---    out_fn     : Output filename                       [optional]
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 

    from time import gmtime, strftime, time
    
    #--- Track progression
    start_time = time()
    
    #--- Initialize
    out =        ['# Created by gen_init_wat.py at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'\n',
                  '# Initial soil moisture as a fraction of saturation point (sm_sat)'+'\n']
                  
    #--- Check parameters    
    if any(i > 1 for i in iw) or any(i < 0 for i in iw):
        #--- Logs Warning and Errors
        import sys
        
        msg   = 'ERROR: The fraction of initial soil moisture provided is out of range (0-1).\n -- Please provide values between 0 and 1.\n -- Initial soil moisture file NOT CREATED.'
        print(msg)
        sys.exit(1)
    
    #--- Append to output
    out.append('         '+'         '.join(["{0:0.4f}".format(i) for i in iw]))
    
    #--- write on file
    with open(out_fn, 'w') as f:
            for item in out:
                f.write("%s" % item)
                
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))
