# -*- coding: utf-8 -*-
"""
#---> Created on Thu Jan 30 11:54:05 2020

#---> @author: Murilo Vianna
"""

#--- Check whether a string s exist in file f_path 
def check_s(f_path, s, has_s = False):
    with open(f_path, "rt") as f:            
        if s in f.read():
            has_s = True
        return has_s
