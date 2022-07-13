# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:55:25 2020

@author: muril
"""

def comp_alg(v_alg,
             df_res,
             c_id = 'sim_code',
             c_dt = 'sim_value'):
    
    #------------------------------------------------------#
    #---------------------- comp_alg ----------------------# 
    #------------------------------------------------------#
    #--- Goal: 
    #---    This function tries to parse the equation given in v_alg arguments and apply to df_res data
    #--- *** Caveats ***
    #---    (1) Calculations are done from left-to-right and only for '+' and '-' operands
    #---    (2) An espace ' ' must be inserted between variables    
    #--- Parameters: 
    #---    v_alg           : Equation (e.g. 'cropstemc + cropreservc + cropleafc')
    #---    df_res          : Panda df with melted results (see get_mp())
    #---    c_id            : Column name of df_res where the variable names are [e.g. 'sim_code']
    #---    c_dt            : Column name of df_res where the simulation results are [e.g. 'sim_value']
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    import numpy as np
    
    #--- initialize
    ini_alg = True
    v_alg_s = np.array(v_alg.split(' '))
    
    #--- compute algebra following the order left to right
    while len(v_alg_s) >= 3:                    
        
        #--- get ids
        a = v_alg_s[0]
        op= v_alg_s[1]
        b = v_alg_s[2]
        
        #--- get data for algebra        
        if ini_alg:
            a_dt    = df_res[c_dt][df_res[c_id] == a].reset_index(drop = True)
            res     = a_dt * 0
            ini_alg = False
        else:
            a_dt = res
    
        b_dt = df_res[c_dt][df_res[c_id] == b].reset_index(drop = True)
                            
        #--- Perform the calculation
        if op == '-':                        
            res  = res + (a_dt - b_dt)
        elif op == '+':
            res  = res + (a_dt + b_dt)
        else:
            print('Warning: Operand symbol "'+str(op)+'" not yet developed for algebra funcionality or not recognized.\nThe operands accepted are: + and -\n --- Algebra for "'+v_alg+'" not done. Please review your meta file.csv --- ')
        
        #--- bite algebra
        v_alg_s = v_alg_s[2:len(v_alg_s)]
    
    #--- use last variable "b" as mask
    m_dt = df_res[:][df_res[c_id] == b].reset_index(drop = True)
    m_dt[c_dt] = res.values
    m_dt[c_id] = v_alg
    
    return(m_dt)
    