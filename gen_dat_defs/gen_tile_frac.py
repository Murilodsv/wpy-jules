# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:56:18 2020

Goal: Generate the tile fraction file for JULES-Crop simulations

@author: muril
"""

def gen_tile_frac(tf:float,
                  out_fn = 'tile_fraction.dat'):
    
    #---------------------------------------------------------------#
    #------------------------ gen_tile_frac ------------------------# 
    #---------------------------------------------------------------#
    #--- Goal: 
    #---    Generate the tile fraction file for JULES-Crop simulations
    #--- Parameters: 
    #---    it         : List of tile fractions for JULES-Crop Simulations.
    #---    out_fn     : Output filename                       [optional]
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------#

    from time import gmtime, strftime, time
    
    #--- Track progression
    start_time = time()
    
    #--- Initialize
    out =        ['# Created by gen_tile_frac.py at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'\n',
                  '# Tile Fraction'+'\n',
                  '# T1     T2     T3     T4     T5     WHEAT  SOYBE  MAIZE  RICE   T10    T11    T12    T13'+'\n']

    #--- Check inputs
    if out_fn == None:
        out_fn = 'tile_fraction.dat'
        
    if len(tf) > 13:
        msg   = 'More than 13 tile fractions provided.\n -- The only first 13 fractions will be used.'
        print(msg)
    
    if len(tf) < 13:
        tf = tf + [0]*(13 - len(tf))
        msg   = 'Less than 13 tile fractions provided.\n -- Zero values set for missing fraction tiles.'    
        print(msg)
    
    if any(i > 1 for i in tf) or any(i < 0 for i in tf):
        #--- Logs Warning and Errors
        import sys
        
        msg   = 'ERROR: One or more tile fractions provided is out of range (0-1).\n -- Please provide values between 0 and 1.\n -- Tile fraction file NOT CREATED.'
        print(msg)
        sys.exit(1)
    
    #--- Append to output
    out.append('  '+'    '.join(["{0:0.2f}".format(i) for i in tf]))
    
    #--- write on file
    with open(out_fn, 'w') as f:
            for item in out:
                f.write("%s" % item)
                
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))