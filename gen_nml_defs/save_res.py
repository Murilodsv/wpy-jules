# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 13:41:37 2020

@author: muril
"""

def save_res(wd:str,
             run_id:str,
             save_all = False):
    
    #----------------------------------------------------------#
    #------------------------ save_res ------------------------# 
    #----------------------------------------------------------#
    #--- Goal: 
    #---    Save simulation results
    #--- Parameters: 
    #---    wd          : Path where the folder will be created/updated
    #---    run_id      : Run ID that will be the folder name
    #---    save_all    : Save all simulations' files (True) or only outputs (False)
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------# 
    
    import os
    import shutil
    
    #--- Create results folder if not present        
    if not os.path.exists(wd+'/results'): os.mkdir(wd+'/results')
    
    #--- full path
    res_folder = '/results/'+run_id
    
    #--- Erase old data
    try:
        if os.path.exists(wd+res_folder): os.remove(wd+res_folder)
    except:    
        shutil.rmtree(wd+res_folder)
        
    if save_all:    src = wd+'/jules_run'
    else:           src = wd+'/jules_run/namelists/output'
    
    shutil.copytree(src,
                    wd+res_folder)
