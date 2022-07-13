# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:13:39 2020

@author: muril
"""

def scatter_plot(sim,
                 obs,
                 fn_out,
                 vnam    = None,
                 units   = None,
                 p_index = False,
                 p_idx   = None,
                 save_fig= True,
                 v_sub   = None,
                 p_sub   = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"],
                 p_size  = 5):

    #----------------------------------------------------------#
    #---------------------- scatter_plot ----------------------# 
    #----------------------------------------------------------#
    #--- Goal: 
    #---    Plot Simulated vs Observed scatter plot
    #--- Parameters:     
    #--- 	sim      	: Simulated data as vector
    #--- 	obs      	: Observed data as vector
    #--- 	fn_out   	: Filename of figure output
    #--- 	vnam     	: Name of variable
    #--- 	units    	: Units of the variable
    #--- 	p_index  	: Plot Indexes (True/False)
    #--- 	p_idx    	: Indexes to be plotted as dataframe with single row
    #--- 	save_fig 	: Save Figure (True/False)
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------#
    
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    import numpy as np    
    
    #--- Linear regression model
    model = sm.OLS(sim, sm.add_constant(obs)).fit()
    
    #--- Regression parameters
    try:
        a     = model.params[0]
        b     = model.params[1]
    except:
        print('Warning: Only one value to compare, not all statistical indexes can be computed.')
        b     = model.params[0]
        a     = None
        
    #--- check a and b
    if type(a) == type(None):   a = 0 # None
    if a != a:                  a = 0 # nan
    if np.isinf(a):             a = 0 # inf
    
    if type(b) == type(None):   b = 0 # None
    if b != b:                  b = 0 # nan
    if np.isinf(b):             b = 0 # inf
                    
    #--- scatter axis-limits
    min_vals = min(np.append(sim,obs))
    max_vals = max(np.append(sim,obs))
    bord     = (max_vals - min_vals) * 0.04
    
    #--- regression and 1:1 lines
    x_reg   = np.linspace(min_vals, max_vals, 2)
    one_one = np.linspace(min_vals - (max_vals - min_vals), max_vals + (max_vals - min_vals), 2)
        
    plt.figure(figsize=(p_size,p_size))    
    plt.plot(one_one, one_one, '--', c = 'red', linewidth=1, label="1:1 Line")
    
    if type(v_sub) == type(None):
        
        plt.scatter(obs,sim,
            edgecolors='black', 
            facecolors='green',
            linewidths= 0.5,
            label="Simulated")
                
    else:
        
        #--- Do not plot stat indexes
        p_index = False
        
        #--- Check size of indexed vector
        if type(v_sub) == type(None):
            print("Warning: None indexer vector given for scatter plot. All Data will be plotted with same color.")
            v_sub = ['Simulated'] * len(obs)
        if len(v_sub) != len(obs):
            print("Warning: Size of indexer vector given for scatter plot differ from observations. All Data will be plotted with same color.")
            v_sub = ['Simulated'] * len(obs)
        
        col_n = 0                
        for v in list(v_sub.unique()):
            
            if col_n > (len(p_sub) -1):
                print("Warning: Number of color in pallete provided is lower than number of sub indexes to plot. Pallete will reboot.")
                col_n = 0
                
            obs_v = obs[v_sub == v]
            sim_v = sim[v_sub == v]
            col   = p_sub[col_n]
            
            plt.scatter(obs_v,sim_v,
                        edgecolors='black', 
                        facecolors=col,
                        linewidths= 0.5,
                        label=v)
            col_n += 1
        
    plt.plot(x_reg, a + b * x_reg, c = 'blue', linewidth=1, label="Regression")
        
    plt.xlim(min_vals - bord,max_vals + bord)
    plt.ylim(min_vals - bord,max_vals + bord)
    plt.ylabel('Simulated '+str(vnam)+' ('+str(units)+')')
    plt.xlabel('Observed ' +str(vnam)+' ('+str(units)+')')
    
    if p_index:
        
        #--- size and format of strings        
        max_s   = len(max(p_idx.keys(), key=len))
        fmt     = "%"+str(max_s)+"s"
        
        l_idx = []
        for k in p_idx.keys():
            lab_i   = k
            val_i   = p_idx[k].values[0]
            print_v = ((fmt) % str(lab_i))+' = '+(("%6.2f") % float(val_i))
            l_idx.append(print_v)
        idx_text = "\n".join(l_idx)
        
        #--- Add Text to plot
        plt.text(0.05, 0.95,
                 idx_text, 
                 horizontalalignment = 'left',
                 verticalalignment   = 'top',
                 transform=plt.gca().transAxes)
                    
    else:  
        
        #--- Add legend instead of indexes
        plt.legend()
    
    #--- Save figure
    if save_fig:
        
        plt.savefig(fn_out+'.scatter_plot.png', dpi = 500)
        
    #plt.show()
    plt.close()
   