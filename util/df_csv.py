# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:07:10 2020

@author: muril
"""

def df_csv(f:str):
    
    #--------------------------------------------#
    #--- Reads CSV file as a Pandas DataFrame ---#
    #--------------------------------------------#
    #   f   : Input filename (.CSV)
    #--------------------------------------------#
    
    from pandas import DataFrame, read_csv
    
    #--- Open csv as DataFrame
    try:
        df    = DataFrame(read_csv(f))        
    except UnicodeDecodeError:
        df    = DataFrame(read_csv(f, encoding='latin-1'))
        
    return(df)