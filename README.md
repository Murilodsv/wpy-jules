# wrappy-jules
Wrapper in python3 for JULES runs at site locations 

![framework](https://github.com/Murilodsv/wrappy-jules/blob/master/framework.png)

## Dependencies:

This wrapper was developed to operate into HPC systems in Linux and JULES (v5.2). To use in different OS, place the JULES executable for corresponding system into the 'wrappy-jules/sim_db' folder and provide the filename to string variable 'exec_fn' in run_dash.py

The following modules dependencies should also be met to run the model:

- PrgEnv-cray/5.2.40
- cray-netcdf-hdf5parallel/4.3.2
- cray-snplauncher/7.0.4

## Description:
This wrapper uses a collection of CSV files to run JULES namelists and compare with field observations. For doing that, python3 scripts re-creates the JULES namelists, run the model and compare results with observations using statistical indexes of performance [mperf.py]. 
It was mainly tested for local simulations in cropping systems such as soybean, maize, sorghum and sugarcane. However, users have high flexibility to incorporate other systems by adding the corresponding configuration into the sim_db folder.

- An example is ready to run for maize crop in file [run_dash.py](https://github.com/Murilodsv/wrappy-jules/blob/master/run_dash.py)

### Description of steps done by wrappy-jules:
From the example above, simulations are set up by the [dashboard_db.csv](https://github.com/Murilodsv/wrappy-jules/blob/master/dashboard_db.csv) and in [Running Settings](https://github.com/Murilodsv/wrappy-jules/blob/a98ab77a9da17737b23b683ea601cd70c46fbf13/run_dash.py#L16-L29). Each line of [dashboard_db.csv](https://github.com/Murilodsv/wrappy-jules/blob/master/dashboard_db.csv) that has the column value 'run_jules' as 'TRUE' will be selected to run the wrappy-jules framework. The file [dashboard_db.csv](https://github.com/Murilodsv/wrappy-jules/blob/master/dashboard_db.csv) must also provide the indexers names for driving, soil, crop and base data for each simulations, that are located into the folder [sim_db](https://github.com/Murilodsv/wrappy-jules/tree/master/sim_db). Using information provided in both [dashboard_db.csv](https://github.com/Murilodsv/wrappy-jules/blob/master/dashboard_db.csv) and [sim_db](https://github.com/Murilodsv/wrappy-jules/tree/master/sim_db) the script [py_jules_run](https://github.com/Murilodsv/wrappy-jules/blob/master/py_jules_run.py) will:
- Create/update the 'jules_run' folder
- Create namelists and data needed in the 'jules_run'
- Run JULES
- Read netCDF and convert output files into CSV
- Compare with the avaiable field observations
- Save results in the [results](https://github.com/Murilodsv/wrappy-jules/tree/master/results) folder with the corresponding run_id

The file [meta_var](https://github.com/Murilodsv/wrappy-jules/blob/master/meta_var.csv) links the variable names and units between simulated and observed values. Model performance and plots are also saved into the [results](https://github.com/Murilodsv/wrappy-jules/tree/master/results) folder.

