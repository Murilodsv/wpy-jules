# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 12:16:26 2020

@author: muril
"""

def gen_presc_dat(presc_nm:str,
                  var:str,
                  out_fn = None,
                  p      = 8,
                  ndim   = 1):
    
    #--------------------------------------------------------------#
    #------------------------ gen_presc_dat -----------------------# 
    #--------------------------------------------------------------#
    #--- Goal: 
    #---    Generate prescribed data
    #--- Parameters: 
    #---    presc_nm    : CSV filename of data      
    #---    out_fn      : output filename           [optional]
    #---    var         : variable value            [optional]
    #---    p           : number precision          [optional]
    #---    ndim        : number of dimensions      [optional]
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 

    import pandas as pd
    import numpy as np
    from time import gmtime, strftime, time
    
    #--- Track progression
    start_time = time()
    
    #--- Logs Warning and Errors
    erro_msg   = ['Error Logs for prescribed data creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    
    #--- Check arguments
    if not '.csv' in presc_nm:
        
        import sys
        
        #--- Only CSV files accepted for now
        msg = "Error: The input file must be a .csv file."
        print(msg+'\nPrescribed data not created.')
        erro_msg.append(msg)            
        sys.exit(1)
        
    if out_fn == None:
        out_fn = presc_nm.replace(".csv",".dat")
    
    #--- Open csv as DataFrame
    driv_df = pd.DataFrame(pd.read_csv(presc_nm))
    
    #--- generate dimensions
    df  = driv_df[[var]*ndim]
    
    #--- write on file    
    np.savetxt(out_fn, df, fmt = str("%0."+str(p)+"f"))    
        
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))