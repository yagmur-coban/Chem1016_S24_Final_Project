#!/bin/bash
#SBATCH -N 8
#SBATCH -t 08:00:00
#SBATCH -A m4276
#SBATCH -q regular
#SBATCH -C gpu
#SBATCH -G 24

module load vasp/6.3.2-gpu
srun -u -n32 -c32 --cpu-bind=cores -G32 vasp_std > vasp.out
