# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 11:40:08 2020

@author: muril
"""

def check_dependencies(val_check,
                       nml_check,
                       arr_check,                       
                       nnl_check,
                       dpc,
                       base_nml_fn):
    
    import pandas as pd
    
    #--- number of dependecies
    d_l = dpc.replace(" & ","&").split('&') 
        
    #--- Value to check
    v1 = val_check    
    for d in d_l:    
    
        d_i = d.replace('(',"").replace(')',"").split(' ')        
        
        v1_nm = d_i[0] # Var check name
        v2_nm = d_i[2] # Var dependency name
        cond  = d_i[1] # conditional
        
        if '%' in v2_nm:
            #--- dependent variable is in another namelist, update nml,arr,nnl
            v2_nm_l     = v2_nm.split('%')
            if len(v2_nm_l) == 4:
                v2_nm       = v2_nm_l[0]
                nml_check   = v2_nm_l[1]
                arr_check   = int(v2_nm_l[2])
                nnl_check   = int(v2_nm_l[3])
            else:
                print('Warning: Number of indexers for dependent variable '+v2_nm+' is missing. Please make sure "%" is being used correctly in this order: variable%namelist%array_id%n_nml')
        
        #--- Read base nml
        base_nml = pd.DataFrame(pd.read_csv(base_nml_fn))    
        
        #--- get value in nml
        f   = ((base_nml['variable'] == v2_nm) & 
               (base_nml['namelist'] == nml_check) & 
               (base_nml['array_id'] == arr_check) & 
               (base_nml['n_nl']     == nnl_check))
        
        v2 = base_nml['val'][f].values
        if len(v2) > 1:
            print('Warning: Tried to check dependency of variable '+str(v1_nm)+' but more than one value was found on base namelist.\n -- First value was selected, please review dependency rule --')
        v2 = float(v2[0])
        
        if cond   == '<':
            if not v1 < v2:  v1 = v2 - v2 * 0.0001 # decrease 0.01%
        elif cond == '<=':
            if not v1 <= v2: v1 = v2 # cap at v2
        elif cond == '==':
            if not v1 == v2: v1 = v2 # cap at v2
        elif cond == '>' :
            if not v1 > v2:  v1 = v2 + v2 * 0.0001 # increase 0.01%
        elif cond == '>=':
            if not v1 >= v2: v1 = v2 # cap at v2

    if v1 != val_check:
        print('Warning: Parameter '+str(v1_nm)+' was corrected to match the dependency rule.')

    return(v1)
