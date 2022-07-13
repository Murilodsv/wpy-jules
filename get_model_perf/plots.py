# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:46:54 2020

@author: muril
"""

def model_comp_plot(df_plot,
                    x_nm,
                    y_nm,
                    fv_nm,
                    fn_out,
                    size_p   = 8,
                    save_fig = True):
    
    import matplotlib.pyplot as plt
    
    #--- Get sim and obs data
    df_obs = df_plot[:][df_plot['type'] == 'obs']
    df_sim = df_plot[:][df_plot['type'] == 'sim']
    
    #--- get unique var and units
    df_uvar = df_plot[[fv_nm,'units']].drop_duplicates() 
    v_nm = df_uvar[fv_nm].unique()  
    
    #--- compute squared grid
    nf = len(v_nm)
    if not nf % 2 == 0: nf += 1
    
    #--- Initilize plot grid
    fig, axs = plt.subplots(int(nf/2), int(nf/2), figsize=(8, 8))   
    
    v = 0
    for r_f in range(0, int(nf/2)):
        for c_f in range(0,int(nf/2)):
            
            #--- get variable
            var = v_nm[v]
            
            #--- get units
            u   = df_uvar['units'][df_uvar[fv_nm] == var].values[0]
            
            #--- plot simulations as lines
            axs[r_f, c_f].plot(df_sim[x_nm][df_sim[fv_nm] == var],
                               df_sim[y_nm][df_sim[fv_nm] == var],
                               c = 'black', 
                               linewidth=1)
            
            #--- plot observations as markers
            axs[r_f, c_f].scatter(df_obs[x_nm][df_obs[fv_nm] == var],
                                  df_obs[y_nm][df_obs[fv_nm] == var],
                                  edgecolors='black', 
                                  facecolors='green',
                                  linewidths= 0.5)
            
            #--- Axis
            axs[r_f, c_f].set(xlabel = x_nm, 
                              ylabel = var+' ('+str(u)+')')
            
            v += 1
    
    #--- save results
    if save_fig:
        plt.savefig(fn_out+'.png', dpi = 500)
        
        
        

df_plot  = run_perf[run_id+'.sim']['plan']
df_plot  = df_plot.reindex()
df_plot['type'] = 'sim'

df_plot = df_plot.rename(columns = {'sim_value':'value',
                                    'sim_units':'units'})

df_plot['run_id'] = run_id

sim_obs = run_perf[run_id+'.sim_obs']['plan']
obs_dfp = run_perf[run_id+'.sim_obs']['plan']
obs_dfp = obs_dfp.rename(columns = {'obs_value':'value',
                                    'sim_units':'units',
                                    'date_sim' : 'date'})
obs_dfp = obs_dfp.reindex()
obs_dfp['type'] = 'obs'
obs_dfp['run_id'] = run_id

df_plot = df_plot.append(obs_dfp[df_plot.keys()])


add_dt = sim_obs[['sim_code','variable','label_var']].drop_duplicates()


df_plot = pd.merge(df_plot,add_dt, how = 'left', on = 'sim_code')

x_nm  = 'dap'
y_nm  = 'value'
fv_nm = 'label_var'
size_p= 8
fn_out = 'test_comp_plot'

model_comp_plot(df_plot,
                'dap',
                'value',
                'label_var',
                'test_comp_plot',
                size_p   = 8,
                save_fig = True)
        







def scatter_plot(sim,
                 obs,
                 p_idx,
                 fn_out,
                 vnam    = None,
                 units   = None,
                 p_index = True,
                 save_fig= True):
            
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    import numpy as np
    
    #--- Linear regression model
    model = sm.OLS(sim, sm.add_constant(obs)).fit()
    
    #--- Regression parameters
    if len(sim) > 1:
        a     = model.params[0]
        b     = model.params[1]
    else:
        print('Warning: Only one value to compare, not all statistical indexes can be computed.')
        b     = model.params[0]
        a     = None
                    
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
        plt.savefig(fn_out+'.png', dpi = 500)
    
    plt.show()
    




sim_obs = run_perf[run_id+'.sim_obs']['plan']
perf    = run_perf[run_id+'.perf']['plan']

sim     = sim_obs['sim_value'][sim_obs['sim_code'] == 'croplai']
obs     = sim_obs['obs_value'][sim_obs['sim_code'] == 'croplai']
perf    = perf[:][perf['model'] == 'lai']
p_idx   = perf[['r2','d','ef','rmse']]
units   = sim_obs['sim_units'][sim_obs['sim_code'] == 'croplai'].values[0]
vnam    = 'lai' 
fn_out  = wd+'/jules_run/namelists/output/'+str(run_id)+'.'+vnam


scatter_plot(sim,
             obs,
             p_idx,
             fn_out,
             vnam,
             units,
             p_index,
             save_fig)