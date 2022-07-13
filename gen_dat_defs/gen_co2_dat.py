# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:57:05 2020

@author: muril
"""

def gen_co2_dat(co2_nm:str,
                out_fn = None,
                var    = 'co2'):
    
    #--------------------------------------------------------------#
    #------------------------ gen_co2_dat -------------------------# 
    #--------------------------------------------------------------#
    #--- Goal: 
    #---    Generate CO2 prescribed data
    #--- Parameters: 
    #---    co2_nm  : CSV filename of CO2 data      
    #---    out_fn  : output filename           [optional]
    #---    var     : variable value            [optional]
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 

    import pandas as pd
    from time import gmtime, strftime, time
    
    #--- Track progression
    start_time = time()
    
    #--- Logs Warning and Errors
    erro_msg   = ['Error Logs for prescribed CO2 creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    
    #--- Check arguments
    if not '.csv' in co2_nm:
        
        import sys
        
        #--- Only CSV files accepted for now
        msg = "Error: The input file must be an .csv file."
        print(msg+'\nPrescribed CO2 data not created.')
        erro_msg.append(msg)            
        sys.exit(1)
        
    if out_fn == None:
        out_fn = co2_nm.replace(".csv",".dat")
    
    #--- Open csv as DataFrame
    driv_df = pd.DataFrame(pd.read_csv(co2_nm))
    
    #--- write on file
    out = driv_df[var]
    with open(out_fn, 'w') as f:
            for item in out:
                f.write("%0.8f\n" % item)
        
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))