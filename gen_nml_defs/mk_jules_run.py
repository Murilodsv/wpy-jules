# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 09:52:13 2020

@author: muril
"""
 
def mk_jules_run(wd_run:str):
    
    #--------------------------------------------------------------#
    #------------------------ mk_jules_run ------------------------# 
    #--------------------------------------------------------------#
    #--- Goal: 
    #---    Create/Update a folder for running jules
    #--- Parameters: 
    #---    wd      : Path where the folder will be created/updated
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    import os
    
    #--- Erase old data
    try:
        if os.path.exists(wd_run): os.remove(wd_run)
    except:
        import shutil
        shutil.rmtree(wd_run)
            
    #--- Create clean folder
    os.makedirs(wd_run)
    os.makedirs(wd_run+'/namelists')
    os.makedirs(wd_run+'/namelists/data')
    os.makedirs(wd_run+'/namelists/output')
    
    