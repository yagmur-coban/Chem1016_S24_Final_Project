#!/bin/bash
#SBATCH -N 6
#SBATCH -t 02:00:00
#SBATCH -A m4276
#SBATCH -q regular
#SBATCH -C gpu
#SBATCH -G 24

module load vasp/6.3.2-gpu
srun -u -n24 -c32 --cpu-bind=cores -G24 vasp_std > vasp.out
