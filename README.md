# wpy-jules [![DOI](https://zenodo.org/badge/513048223.svg)](https://zenodo.org/badge/latestdoi/513048223)
Wrapper in python3 for JULES runs at site locations 

![framework](https://github.com/Murilodsv/wrappy-jules/blob/main/framework.png)

## Dependencies:

This wrapper was developed to operate into HPC systems in Linux and JULES (v5.2). To use in different OS, place the JULES executable for corresponding system into the 'wrappy-jules/sim_db' folder and provide the filename to string variable 'exec_fn' in run_dash.py

The following modules dependencies should also be met to run the model:

- PrgEnv-cray/5.2.40
- cray-netcdf-hdf5parallel/4.3.2
- cray-snplauncher/7.0.4

## Description:
This wrapper uses a collection of CSV files to run JULES namelists and compare with field observations. For doing that, python3 scripts re-creates the JULES namelists, run the model and compare results with observations using statistical indexes of performance [mperf.py]. 
It was mainly tested for local simulations in cropping systems such as soybean, maize, sorghum and sugarcane. However, users have high flexibility to incorporate other systems by adding the corresponding configuration into the sim_db folder.

- An example is ready to run for sugarcane crop in file [run_dash.py](https://github.com/Murilodsv/wrappy-jules/blob/main/run_dash.py)
- It is also possible to pass running arguments to run_dash.py like:

```
python run_dash.py SC1072,SC1003 example_sc dashboard_db.csv
```

### Description of steps done by wrappy-jules:
From the example above, simulations are set up by the [dashboard_db.csv](https://github.com/Murilodsv/wrappy-jules/blob/main/dashboard_db.csv) and in [Running Settings](https://github.com/Murilodsv/wrappy-jules/blob/277df71f1aa16bac6ed20ea0e596daff8624c0e6/run_dash.py#L18-L39). Each line of [dashboard_db.csv](https://github.com/Murilodsv/wrappy-jules/blob/main/dashboard_db.csv) that has the column value 'run_jules' as 'TRUE' will be selected to run the wrappy-jules framework. The file [dashboard_db.csv](https://github.com/Murilodsv/wrappy-jules/blob/main/dashboard_db.csv) must also provide the indexers names for driving, soil, crop and base data for each simulations, that are located into the folder [sim_db](https://github.com/Murilodsv/wrappy-jules/tree/main/sim_db). In summary, the steps are:
- Create/update the 'jules_run' folder
- Create namelists and data needed in the 'jules_run'
- Run JULES
- Read netCDF and convert output files into CSV
- Compare with the avaiable field observations
- Save results in the [jules_run](https://github.com/Murilodsv/wrappy-jules/tree/main/jules_run) folder with the corresponding run_id

The file [meta_var](https://github.com/Murilodsv/wrappy-jules/blob/main/meta_var.csv) links the variable names and units between simulated and observed values. Model performance and plots are also saved into the [jules_run](https://github.com/Murilodsv/wrappy-jules/tree/main/jules_run) folder.

### Extras:

Generalized calibration methods are incorporated in [run_cali.py](https://github.com/Murilodsv/wrappy-jules/blob/main/run_cali.py). An example of how to calibrate SLA-related parameters for a given site can be ran by:

```
python run_cali.py SC1072 calib-sla-example T lai rmse calibration_setup_sla.csv T
```

In the above code the arguments represent:
- the site to be considered: SC1072 (more than one site can be provided separated by comma)
- the calibration id name: calib-sla-example
- flag indicating calibration run: T
- observed variable used to calculate the objective function: lai (more than one variable can be provided separated by comma. If so, make sure the units/magnitudes match!)
- the statistical index used as objective function: rmse (available indexers are calculated in [mperf.py](https://github.com/Murilodsv/wrappy-jules/blob/main/get_model_perf/mperf.py). If d, r2 or ef are selected objective function becomes = 1 - stat_index)
- the target parameters to be calibrated, including max-min ranges: [calibration_setup_sla.csv](https://github.com/Murilodsv/wrappy-jules/blob/main/calibration_setup_sla.csv)
- flag indicating calibration run: T

### Publications using this repository:

- Prudente Jr et al. (2022). Calibration and evaluation of JULES-crop for maize in Brazil. Agronomy Journal. https://doi.org/10.1002/agj2.21066

- Vianna et al. (2022). Improving the representation of sugarcane crop in the JULES model for climate impact assessment. Global Change Biology Bioenergy. https://doi.org/10.1111/gcbb.12989
