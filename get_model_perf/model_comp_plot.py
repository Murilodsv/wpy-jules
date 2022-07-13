# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:43:32 2020

@author: muril
"""

def model_comp_plot(df_plot,
                    x_nm,
                    y_nm,
                    fv_nm,
                    hue_nm,
                    fn_out,
                    save_fig = True,
                    v_sub    = None,
                    p_sub    = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"],
                    size_p   = 4,
                    t_fsize  = 20,
                    t_ypos   = 0.93,
                    dpi_fig  = 300):
    
    #-------------------------------------------------------#
    #-------------------- model_comp_plot ------------------# 
    #-------------------------------------------------------#
    #--- Goal: 
    #---    Plot Simulated (lines) and Observed (markers) data against time
    #--- Parameters: 
    #--- 	df_plot 	: dataframe with simulated and observed data for one or more variables
    #--- 	x_nm    	: Name of df_plot column to use as X axis
    #--- 	y_nm    	: Name of df_plot column to use as Y axis
    #--- 	fv_nm   	: Name of df_plot column to be split in different facets
    #---    hue_nm      : Name of df_plot column to be used as hue
    #--- 	fn_out  	: Filename of output figure
    #--- 	save_fig	: Save Figure (True/False)
    #--- 	size_p  	: Size of facet
    #--- 	t_fsize 	: Title fontsize
    #--- 	t_ypos  	: Title vertical position
    #--- 	dpi_fig 	: Figure Resolution 
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #-------------------------------------------------------#    
    
    import matplotlib.pyplot as plt
    import numpy as np    
    from matplotlib.ticker import FormatStrFormatter
    
    #--- Get sim and obs data
    df_obs = df_plot[:][df_plot['type'] == 'obs']
    df_sim = df_plot[:][df_plot['type'] == 'sim']
    
    #--- get unique var and units
    df_uvar = df_plot[[fv_nm,'units']].drop_duplicates() 
    v_nm = df_uvar[fv_nm].unique()  
    
    #--- attribute unique colors to each hue
    hue_cols = {}
    c_i      = 0    
    for h in df_plot[hue_nm].unique():
        hue_cols[h] = p_sub[c_i]
        c_i +=1
        if (c_i+1) > len(p_sub): c_i = 0    
    
    #--- compute squared grid
    nv = len(v_nm)    
    if np.sqrt(nv) - int(np.sqrt(nv)) == 0:
        nr_f = int(np.sqrt(nv))
        nc_f = int(np.sqrt(nv))
    else:
        nc_f = int(np.sqrt(nv))+1
        nr_f = int(nv / nc_f) + 1        
        
    if nr_f * nc_f - nv == np.sqrt(nr_f * nc_f):
        nr_f = nr_f - 1    
        
    x_size = nc_f   * size_p
    y_size = nr_f   * size_p
        
    #--- Initilize plot grid
    fig, axs = plt.subplots(nr_f, nc_f, figsize=(x_size, y_size))   
        
    v = 0
    add_leg = True
    l_leg   = []
    for r_f in range(0, nr_f):
        for c_f in range(0,nc_f):
            
            #--- get axis obj
            if (nr_f * nc_f) == 1:      axs_rc = axs
            elif (nr_f * nc_f) == 2:    axs_rc = axs[c_f]            
            else:                       axs_rc = axs[r_f, c_f]
            
            if (v+1) <= len(v_nm):               
                
                #--- get variable
                var = v_nm[v]
                
                #--- get units
                u   = df_uvar['units'][df_uvar[fv_nm] == var].values[0]
                
                #--- plot simulations as lines                
                for h in df_sim[hue_nm].unique():
                    f = (df_sim[fv_nm] == var) & (df_sim[hue_nm] == h)                    
                    axs_rc.plot(df_sim[x_nm][f],
                                df_sim[y_nm][f],
                                c = hue_cols[h], 
                                linewidth=1)
                
                #--- plot observations as markers                
                for h in df_obs[hue_nm].unique():
                    
                    l = None
                    if add_leg:
                        l = h
                        l_leg = l_leg + [l]
                    
                    f = (df_obs[fv_nm] == var) & (df_obs[hue_nm] == h)                    
                    axs_rc.scatter(df_obs[x_nm][f],
                                   df_obs[y_nm][f],
                                   edgecolors='black', 
                                   facecolors=hue_cols[h],
                                   linewidths= 0.5,
                                   label = l)
                
                if add_leg and set(l_leg).issubset(df_obs[hue_nm]):
                    #axs[r_f, c_f].legend() 
                    #fig.legend(loc = 'lower center', ncol = 4)
                    add_leg = False
                    
                #--- Axis
                axs_rc.set(xlabel = x_nm, 
                           ylabel = var+' ('+str(u)+')')
                
                #--- get limits
                max_vals = []
                min_vals = []
                if len(df_sim[y_nm][df_sim[fv_nm] == var].values) > 0: 
                    max_vals = max_vals + [max(df_sim[y_nm][df_sim[fv_nm] == var].values)]
                    min_vals = min_vals + [min(df_sim[y_nm][df_sim[fv_nm] == var].values)]
                    
                if len(df_obs[y_nm][df_obs[fv_nm] == var].values) > 0: 
                    max_vals = max_vals + [max(df_obs[y_nm][df_obs[fv_nm] == var].values)]
                    min_vals = min_vals + [min(df_obs[y_nm][df_obs[fv_nm] == var].values)]
                                
                max_y = max(max_vals)                
                min_y = min(min_vals)
                
                if max_y - min_y < 0.01:
                    m_point = np.mean([max_y,min_y])
                    axs_rc.ylim([m_point-0.01, m_point+0.01])
                
                if max_y < 10:                
                    axs_rc.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
                elif max_y < 100:
                    axs_rc.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
                elif max_y < 1000:
                    axs_rc.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
                
            else:
                #--- delete blank axis
                fig.delaxes(axs_rc)
            
            v += 1
        
    #fig.tight_layout()
    if (nr_f * nc_f) <= 2:
        fig.legend(loc = 'upper center', ncol = 4)        
    else:        
        fig.legend(loc = 'lower center', ncol = 4)
    
    #--- save results
    if save_fig:
        plt.savefig(fn_out+'.comp_plot.png', dpi = dpi_fig)
        
    #plt.show()
    plt.close()
    
