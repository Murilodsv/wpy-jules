# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:20:46 2020

@author: muril
"""

def fortran_bool(f):
    
    true_keys  = ['T','True','TRUE','.true.','.TRUE.','true']
    false_keys = ['F','False','FALSE','.false.','.FALSE.','false']
    
    if f in true_keys:
        return(True)    
    if f in false_keys:
        return(False)
    
    print('Warning: Variable "'+f+'" added as boolean but is not recognized.')
    return(f)
        
    