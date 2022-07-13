# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 13:33:47 2020

@author: muril
"""

def get_mp_all(sim_id,
               all_per,
               df_plot_all,
               wd,
               v_f      = 'variable',
               save_res = True,
               x_nm     = 'dap',
               y_nm     = 'value',
               fv_nm    = 'label_var',
               hue_nm   = 'run_id',
               fn_out   = 'comp_fig',
               save_fig = True,
               size_p   = 5,
               t_fsize  = 20,
               t_ypos   = 0.93,
               dpi_fig  = 300,
               f_plot_perf = True):

    from get_model_perf import mperf
    import get_model_perf as mp
    import pandas as pd
    
    print('\n!---------------------------------!'+
          '\n!--- Overall Model Performance ---!'+
          '\n!---------------------------------!\n')
           
    #--- Overall Performance
    l_sim_obs = [all_per[s] for s in all_per.keys() if ".sim_obs" in s]
    
    #--- Bind all sim_obs
    init_all_sim_obs = True
    for so in l_sim_obs:
        
        if init_all_sim_obs:
            all_sim_obs      = so
            init_all_sim_obs = False
        else:
            
            for k_so in so.keys():
                if type(so[k_so]) != type(None):                
                    
                    try:
                        if type(all_sim_obs[k_so]) == type(None):
                            all_sim_obs[k_so] = so[k_so]
                        else:
                            all_sim_obs[k_so] = all_sim_obs[k_so].append(so[k_so])
                    except KeyError:
                        all_sim_obs[k_so] = so[k_so]
    
    init_perf = True
    for k in all_sim_obs.keys():
        if type(all_sim_obs[k]) != type(None):
            
            #--- Sim and Obs data
            sim_obs_df = all_sim_obs[k]
            
            #--- list of variables
            l_var = sim_obs_df[v_f].unique()
            
            for v in l_var:
                
                print('Computing overall performance of '+v)
                
                #--- Units
                u = sim_obs_df['sim_units'][sim_obs_df[v_f] == v].values[0]
                
                #-----------------------------#
                #--- Get performance as df ---#
                #-----------------------------#
                perf_v = pd.DataFrame(mperf(sim    = sim_obs_df['sim_value'][sim_obs_df[v_f] == v],
                                            obs    = sim_obs_df['obs_value'][sim_obs_df[v_f] == v],
                                            vnam   = v,
                                            dchart = False), index=[0])
                
                if f_plot_perf:
                    #--------------------#
                    #--- plot results ---#
                    #--------------------#
                    mp.scatter_plot(sim     = sim_obs_df['sim_value'][sim_obs_df[v_f] == v],
                                    obs     = sim_obs_df['obs_value'][sim_obs_df[v_f] == v],                         
                                    fn_out  = fn_out+'.'+str(k)+'.'+str(v),
                                    vnam    = v,
                                    units   = u,
                                    p_index = False,
                                    p_idx   = None,
                                    save_fig= True,
                                    v_sub   = sim_obs_df['run_id'][sim_obs_df[v_f] == v],
                                    p_size  = 5)
                
                #--- Bind performance results
                if init_perf:
                    perf_df   = perf_v
                    init_perf = False        
                else:                
                    perf_df   = perf_df.append(perf_v)
            
            #--- Add key ID
            perf_df['key'] = k
    
    if save_res:
        perf_df['sim_id'] = sim_id
        perf_df['run_id'] = 'ensemble'        
        
        #--- bind individual performance
        l_perf = [all_per[s] for s in all_per.keys() if ".perf" in s]
            
        #--- Bind all perf to a single dic
        init_all_l_perf = True
        for so in l_perf:
            
            if init_all_l_perf:
                all_l_perf       = so
                init_all_l_perf  = False
            else:
                
                for k_so in so.keys():
                    if type(so[k_so]) != type(None):                
                        
                        try:
                            if type(all_l_perf[k_so]) == type(None):
                                all_l_perf[k_so] = so[k_so]
                            else:
                                all_l_perf[k_so] = all_l_perf[k_so].append(so[k_so])
                        except KeyError:
                            all_l_perf[k_so] = so[k_so]
        
        #--- collapse all dic to a single df
        init_all_l_perf = True
        for so in all_l_perf:
            if type(all_l_perf[so]) != type(None):
                d_so = all_l_perf[so]
                d_so['key']    = so
                d_so['sim_id'] = sim_id
                
                if init_all_l_perf:
                    all_l_perf_df   = d_so
                    init_all_l_perf = False
                else:
                    all_l_perf_df = all_l_perf_df.append(d_so)   
        
        #--- bind overall performance with individual perf
        perf_df = perf_df.append(all_l_perf_df[perf_df.keys()])
        
        #--- write performance
        perf_df.to_csv(fn_out+'.model_performance.csv', index = None, header=True)

    if f_plot_perf:
        for k in df_plot_all['class'].unique():    
            
            print('Ploting comparison for '+k)
            
            #--- sub plot
            df_plot = df_plot_all[:][df_plot_all['class'] == k]
            
            #--- order by name        
            df_plot = df_plot.sort_values(by=[fv_nm,x_nm])
            
            #--- Plot all comparison
            mp.model_comp_plot(df_plot,
                               x_nm   = x_nm,
                               y_nm   = y_nm,
                               fv_nm  = fv_nm,
                               hue_nm = hue_nm,
                               fn_out = fn_out+'.'+k,
                               save_fig = save_fig,
                               size_p   = size_p,
                               t_fsize  = t_fsize,
                               t_ypos   = t_ypos,
                               dpi_fig  = dpi_fig)
        