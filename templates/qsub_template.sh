#!/bin/bash -l

#PBS -N <sim_id>
#PBS -o <sim_id>.out
#PBS -e <sim_id>.err
#PBS -S /bin/bash
#PBS -W umask=0022
#PBS -q shared
#PBS -l ncpus=1
#PBS -l walltime=<walltime>

cd ~/py-jules

python run_dash.py <csv_run_ids> <sim_id> <dash_db>

