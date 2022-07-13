# -*- coding: utf-8 -*-
"""
#------------------------------------#
#--- Generate namelists for JULES ---#
#------------------------------------#

#---> Created on Wed Jan 15 15:33:07 2020

#---> @author: Murilo Vianna (murilodsv@gmail.com)
"""

def gen_nml(setup_fn:str,
            tnml_path= None,
            out_path = None):

    #--------------------------------------------------------#
    #------------------------ gen_nml -----------------------# 
    #--------------------------------------------------------#
    #--- Goal: 
    #---    Generate the namelists files for JULES simulation
    #--- Parameters: 
    #---    setup_fn    : Input .CSV file containing all namelists info
    #---    tnml_path   : Input folder where the .nml templates are located
    #---    out_path    : Output path where .nml files will be generated 
    #--- Dependencies:    
    #---    gen_nml_defs
    #---    template files (.nml)
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    #--- Load Global Packages
    import pandas as pd
    import os
    from time import gmtime, strftime, time
    
    #--- Load internal Packages
    import gen_nml_defs as gd
    
    #--- Track progression
    start_time = time()
    warn_msg   = ['Warning Logs for Namelist creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    erro_msg   = ['Error Logs for Namelist creation at '+strftime("%Y-%m-%d %H:%M:%S", gmtime())+":\n"]
    
    #--- Check arguments
    if not '.csv' in setup_fn:
        import sys        
        #--- Only CSV files accepted for now
        msg = "Error: The template setup file must be an .csv file."
        print(msg+'\nNamelists not created.')
        erro_msg.append(msg)            
        sys.exit(1)
    
    #--- Open csv as DataFrame with variables setup
    var_setup = pd.DataFrame(pd.read_csv(setup_fn))
    
    #--- Convert NaNs to ''
    var_setup = var_setup.fillna('')
    
    #--- Get list of namelists files
    l_nlf   = var_setup['file'].unique().tolist()
    
    #--- Create namelists
    for nlf in l_nlf:
            
        #--- Get list of namelists per file    
        l_nl    = var_setup.loc[var_setup['file'] == nlf,'namelist'].unique().tolist()
        
        #--- open namelist file template and store in array
        finp        = open(tnml_path+'/template_'+nlf, "rt")
        temp_array  = finp.readlines()
        
        #--- close template
        finp.close()
        
        #--- Create each namelist
        for nl in l_nl:
                                        
            #--- Check if namelist exist in template section
            if not gd.check_s(tnml_path+'/template_'+nlf, '&'+nl):
                
                msg = 'Warning: Namelist "'+nl+'" not found on template file "template_'+nlf+'"'
                print(msg)
                warn_msg.append(msg)
                # Call warning log
            else:
                
                #--- Retrieve data from var setup            
                l_fin_nl = var_setup.loc[(var_setup['file'] == nlf) & (var_setup['namelist'] == nl),'temp_var']                       
                l_nnl_nl = var_setup.loc[(var_setup['file'] == nlf) & (var_setup['namelist'] == nl),'n_nl'    ]
                
                #--- find unique (templates will have only unique values per namelist i.e. the repetitions are arrays!)
                l_fin_nl_u = list(set(l_fin_nl))
                
                #--- namelist length 
                len_finp = l_fin_nl_u.__len__()
                
                #--- Check if this namelist should be repeated (e.g. output profiles)
                repeat_nl = len(set(l_nnl_nl)) > 1         
                
                #--- Initialize
                create_nl = True
                found_nl  = False
                start_nl  = False            
                found_var = 0
                n_nl      = 0
                l         = 0
                
                #--- Loop-over the namelist file template
                while create_nl:
                    
                    #--- flag of namelist begin
                    if temp_array[l].find('&'+nl) == 0:
                        start_nl = True
                        found_nl = True
                        l+=1
                        if repeat_nl:
                            #--- Update l_fin_nl_u, namelist length and n_nl 
                            n_nl+=1
                            l_fin_nl_u  = list(set(l_fin_nl[l_nnl_nl == n_nl]))
                            len_finp    = l_fin_nl_u.__len__()                                                
                    
                    #--- flag of namelist end
                    if temp_array[l].find('/') == 0 and found_nl:
                        create_nl = False
                        start_nl  = False
                        if repeat_nl and n_nl <= len(set(l_nnl_nl)):
                            #--- Keep looking for repeated nl
                            create_nl = True
                            if n_nl == len(set(l_nnl_nl)): 
                                create_nl = False
                    
                    #--- We are at namelist, try to find/replace
                    if start_nl:
                        for l_i in l_fin_nl_u:                        
                            if temp_array[l].find(l_i) >= 0: # -1 = not found
                                
                                #-----------------#
                                #--- Found Ya! ---#
                                #-----------------#
                                
                                #--- Find Variable
                                fin_var = l_i
                                
                                #--- Extract values
                                rep_var = gd.get_var_setup(var_setup, nlf, nl, n_nl, fin_var)
                                    
                                temp_array[l] = temp_array[l].replace(fin_var,rep_var)
                                found_var+=1
                         
                    #--- next line
                    l+=1
                    
                    #--- When reach last line check if any namelist were found
                    if l > (temp_array.__len__()-1):
                        
                        if not found_nl:
                            msg = 'Warning: Namelist "'+nl+'" not found on template file "template_'+nlf+'"'
                            print(msg)
                            warn_msg.append(msg)
                        
                        if start_nl:
                            msg = 'Warning: Namelist "'+nl+'" found but could not find the "/" closure on template file "template_'+nlf+'"'
                            print(msg)
                            warn_msg.append(msg)
                            
                        #--- get out of loop
                        create_nl = False
        
        #----------------------#
        #--- Write Namelist ---#
        #----------------------#
        with open(out_path+'/'+nlf, 'w') as f:
            for item in temp_array:
                f.write("%s" % item)    
        
        msg = "File "+nlf+" created."
        print(msg)
    
    #--- Check progression
    if len(warn_msg) > 1:
        
        #--- Warnings found
        print('Namelists created at namelists/ but some warnings were generated and can be found at file: warnings_gen_nml.wng')
        with open('warnings_gen_nml.wng', 'w') as f:
            for item in warn_msg:
                f.write("%s\n" % item)
                
    else:
        #--- No Warnings        
        if os.path.exists('warnings_gen_nml.wng'):
            os.remove('warnings_gen_nml.wng')    
        
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))
