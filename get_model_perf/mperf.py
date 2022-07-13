# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:43:05 2020

@author: murilo vianna
"""

def mperf(sim,
          obs,
          vnam   = '',
          dchart = True,
          outidx = "all"):

    #--------------------------------------------------#
    #------------- Performance function ---------------#
    #--- Compute statistical indexes of performance ---#
    #--------------------------------------------------#
    #
    # Decription:
    # sim     - Simulated values          [Real]
    # obs     - Observed values           [Real]
    # vnam    - Name of variable          [String]
    # dchart  - Display Chart?            [T or F]
    # outidx  - Output peformance indexes [List]
    # 
    # Murilo Vianna
    # source: https://github.com/Murilodsv/R-scripts/blob/master/mperf.r
    #
    # Literature: 
    # Brun, F., Wallach, D., Makowski, D., & Jones, J. W. (2006). 
    # Working with dynamic crop models: evaluation, analysis, 
    # parameterization, and applications. Elsevier.
    #--------------------------------------------------#
    
    import numpy as np
    import statsmodels.api as sm
    
    #--- all outputs
    if outidx[1] == "all":
        outidx = ["bias","mse","rmse","mae","rrmse","rmae","ef","r","r2","d","cc","a","b","mi_sim","sd_sim","cv_sim","mi_obs","sd_obs","cv_obs","n"]
    
    #--- Check Input data
    sim = np.array(sim, dtype=float)
    obs = np.array(obs, dtype=float)
    
    if len(sim) != len(obs):        
        import sys        
        #--- Only CSV files accepted for now
        msg = "Error in mperf(): Vector length of Simulated and Observed do not match."
        print(msg)
        sys.exit(1)
    
    if any(np.isnan(sim)): sim = sim[~np.isnan(sim)]; obs = obs[~np.isnan(sim)]
    if any(np.isnan(obs)): sim = sim[~np.isnan(obs)]; obs = obs[~np.isnan(obs)]
        
    #--- Statistical indexes
    n     = len(obs)
    mi_sim= np.mean(sim)
    mi_obs= np.mean(obs)
    bias  = (1/n) * np.sum(sim-obs)
    mse   = (1/n) * np.sum((sim-obs)**2)
    rmse  = np.sqrt(mse)
    mae   = (1/n) * np.sum(np.abs(sim-obs))
    rrmse = rmse / np.mean(obs)
    rmae  = (1/len(obs[obs>0])) * np.sum(np.abs(sim[obs>0]-obs[obs>0])/np.abs(obs[obs>0]))
    ef    = 1 - (np.sum((sim-obs)**2) / np.sum((obs-np.mean(obs))**2))
    r     = np.sum((obs-np.mean(obs))*(sim-np.mean(sim)))/np.sqrt(np.sum((obs-np.mean(obs))**2)*np.sum((sim-np.mean(sim))**2))
    r2    = r**2
    d     = 1 - (np.sum((sim-obs)**2) / np.sum((np.abs(sim-np.mean(obs))+np.abs(obs-np.mean(obs)))**2))
    
    sigma_obs_sim   = (1 / n) * np.sum((obs - mi_obs) * (sim - mi_sim))
    sigma_obs_2     = (1 / n) * np.sum((obs - mi_obs) ** 2)
    sigma_sim_2     = (1 / n) * np.sum((sim - mi_sim) ** 2)
    cc              = (2 * sigma_obs_sim) / (sigma_obs_2 + sigma_sim_2 + (mi_sim - mi_obs)**2)
    
    sd_obs = np.std(obs)
    sd_sim = np.std(sim)
    cv_obs = sd_obs / mi_obs
    cv_sim = sd_sim / mi_sim
        
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
    
    #--- Stat indexes
    aic   = model.aic
    bic   = model.bic
    pval  = model.f_pvalue
    fval  = model.fvalue
    
    if dchart:
        
        import matplotlib.pyplot as plt        
        
        min_vals = min(np.append(sim,obs))
        max_vals = max(np.append(sim,obs))
        bord     = (max_vals - min_vals) * 0.04
        
        x_reg   = np.linspace(min_vals, max_vals, 2)
        one_one = np.linspace(min_vals - (max_vals - min_vals), max_vals + (max_vals - min_vals), 2)
        
        
        plt.plot(one_one, one_one, '--', c = 'red', linewidth=1, label="1:1 Line")        
        plt.scatter(obs,sim,
                    edgecolors='black', 
                    facecolors='green',
                    linewidths= 0.5,
                    label="Simulated ")             
        plt.plot(x_reg, a + b * x_reg, c = 'blue', linewidth=1, label="Regression")
        plt.xlim(min_vals - bord,max_vals + bord)
        plt.ylim(min_vals - bord,max_vals + bord)
        plt.ylabel('Simulated '+str(vnam))
        plt.xlabel('Observed ' +str(vnam))
        plt.legend()
        plt.show()
        #plt.savefig('mperf.png', dpi = 500)
    
    perf = {'model' : vnam   ,
            'bias'  : bias   ,
            'mse'   : mse    ,
            'rmse'  : rmse   ,
            'mae'   : mae    ,
            'rrmse' : rrmse  ,
            'rmae'  : rmae   ,
            'ef'    : ef     ,
            'r'     : r      ,
            'r2'    : r2     ,
            'd'     : d      ,
            'cc'    : cc     ,
            'a'     : a      ,
            'b'     : b      ,
            'aic'   : aic    , 
            'bic'   : bic    ,
            'pval'  : pval   ,
            'fval'  : fval   ,
            'mi_sim': mi_sim ,
            'sd_sim': sd_sim ,
            'cv_sim': cv_sim ,
            'mi_obs': mi_obs ,
            'sd_obs': sd_obs ,
            'cv_obs': cv_obs ,
            'n'     : n}
    
    return(perf)  
