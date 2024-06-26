#!/bin/bash -l        
#SBATCH --time=16:00:00
#SBATCH --ntasks=8
#SBATCH --mem=10g
#SBATCH --tmp=10g
#SBATCH --mail-type=ALL  
#SBATCH --mail-user=reine097@umn.edu 
#SBATCH -e chirality_correction_for_fold-%j.err
#SBATCH -o chirality_correction_for_fold-%j.out

cd /home/miran045/reine097/projects/SynthSeg/SynthSeg/dcan/img_processing/chirality_correction/ || exit
export PYTHONPATH="${PYTHONPATH}:/home/miran045/reine097/projects/SynthSeg"
/home/faird/shared/code/external/envs/miniconda3/mini3/envs/SynthSeg/bin/python \
	/home/miran045/reine097/projects/SynthSeg/SynthSeg/dcan/img_processing/chirality_correction/chirality_correction_for_fold.py
