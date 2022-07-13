# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 21:25:28 2020

@author: muril
"""

def format_var(var,
               t_var:{'integer','real','character','logical'},
               p_var:int) -> str:
    
    #-------------------------------------------------------------#
    #------------------------ format_var -------------------------# 
    #-------------------------------------------------------------#
    #--- Goal: 
    #---    Format replaceable variable to namelist format (fortran namelists)
    #--- Parameters:            
    #---    var     : variable value
    #---    t_var   : type of value {'integer','real','character','logical'}
    #---    p_var   : precision when value is a float (real)
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
                
    if t_var == "integer":
        #--- Truncate and convert to string
        res_var = str(int(var))
    
    elif t_var == "real":
        #--- Format float to decimals and convert to string        
        if len(str(var)) > (p_var+2):
            #--- write in scientific notation when number of characters is higher than precision
            if float('%.1E'%(float(var))) == float(var):
                #--- No need for all decimals
                res_var = ("%.1E") % float(var)
            else:
                #--- Use provided precision
                res_var = ("%."+str(int(p_var))+"E") % float(var)
        else:            
            if float('%.1f'%(float(var))) == float(var):
                #--- No need for all decimals
                res_var = ("%.1f") % float(var)
            else:
                #--- Use provided precision
                res_var = str(float(var))
        
        #--- Check output
        if float(res_var) != float(var):
            msg = "Warning: Value "+str(var)+" changed to "+str(res_var)+"."
            print(msg)
            
    elif t_var == "character":
        #--- write string within quotes
        res_var = str(var)
        
    elif t_var == "logical":
        #--- write string within quotes
        res_var = str(var)
        
    else:                
        msg = "The type "+t_var+" for variable "+var+" is not supported."
        print(msg)
        res_var = str(var)
        
    return res_var

def get_var_setup(var_setup, 
                  nlf: str, 
                  nl:  str, 
                  n_nl:int, 
                  fin_var:str) -> str:
    
    #----------------------------------------------------------------#
    #------------------------ get_var_setup -------------------------# 
    #----------------------------------------------------------------#
    #--- Goal: 
    #---    Extract value from var_setup df to replace in namelist template
    #--- Variables:            
    #---    var_setup   : df with variables setup
    #---    nlf         : namelist file name
    #---    nl          : namelist name
    #---    n_nl        : number of repeated namelist with same name within this namelist file (e.g. output.nml)
    #---    fin_var     : temp_var to be find
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
        
    #--- Lookup variable
    df_var = var_setup[(var_setup['temp_var' ].isin([fin_var])) & 
                       (var_setup['n_nl'     ].isin([n_nl   ])) &
                       (var_setup['file'     ].isin([nlf    ])) &
                       (var_setup['namelist' ].isin([nl     ]))]
    
    #--- Check if variable is an array            
    if len(df_var) > 1:
        
        #----------------------#
        #--- Array variable ---#
        #----------------------#
        
        #--- sort df by array_id 
        df_var   = df_var.sort_values(by='array_id')
        l_arr_id = df_var['array_id']
        
        #--- Check if array_id conforms
        if len(df_var) != len(df_var['array_id'].unique()):
            msg = "Warning: Number of values for variable "+fin_var+" do not match with it's array_id."
            print(msg)
            
        #--- Construct array res
        res = ""
        for arr_id in l_arr_id:
            
            var   = df_var['val' ][df_var['array_id'].isin([arr_id])].values[0]
            t_var = df_var['type'][df_var['array_id'].isin([arr_id])].values[0]
            p_var = df_var['prec'][df_var['array_id'].isin([arr_id])].values[0]
            
            if not arr_id == l_arr_id.iloc[len(l_arr_id)-1]:
                res = res + format_var(var, t_var, p_var) + ","
            else:
                res = res + format_var(var, t_var, p_var)                
        
    elif len(df_var) == 1:
        
        #--------------------#
        #--- Single Value ---#
        #--------------------#
        
        var   = df_var['val' ].values[0]
        t_var = df_var['type'].values[0]
        p_var = df_var['prec'].values[0]
        
        res = format_var(var, t_var, p_var)
        
    else:
        msg = 'Warning: There is no temp_var "'+fin_var+'" not found on template file "template_'+nlf+'"'
        print(msg)
        res = "ERROR: "+msg
    
    return res
            
        