#!/bin/bash -l        
#SBATCH --time=0:30:00
#SBATCH --ntasks=8
#SBATCH --mem=10g
#SBATCH --tmp=10g
#SBATCH --mail-type=ALL  
#SBATCH --mail-user=reine097@umn.edu 
#SBATCH -e correct_chirality-%j.err
#SBATCH -o correct_chirality-%j.out

cd /home/miran045/reine097/projects/SynthSeg/SynthSeg/dcan/img_processing
export PYTHONPATH="${PYTHONPATH}:/home/miran045/reine097/projects/SynthSeg"
/home/faird/shared/code/external/envs/miniconda3/mini3/envs/SynthSeg/bin/python \
	/home/miran045/reine097/projects/SynthSeg/SynthSeg/dcan/img_processing/correct_chirality.py
