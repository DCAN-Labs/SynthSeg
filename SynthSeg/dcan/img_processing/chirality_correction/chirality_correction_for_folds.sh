#!/bin/bash
sbatch <<EOT
#!/bin/sh

#SBATCH --job-name=chirality_correction_for_folds
#SBATCH --time=24:00:00
#SBATCH --ntasks=8
#SBATCH --mem=10g
#SBATCH --tmp=10g
#SBATCH --mail-type=ALL
#SBATCH --mail-user=reine097@umn.edu
#SBATCH -e chirality_correction_for_folds-%j.err
#SBATCH -o chirality_correction_for_folds-%j.out

cd /home/miran045/reine097/projects/SynthSeg/SynthSeg/dcan/img_processing/chirality_correction/ || exit
export PYTHONPATH="${PYTHONPATH}:/home/miran045/reine097/projects/SynthSeg"
module load python3
module load fsl
module load ants
/home/miran045/reine097/projects/SynthSeg/venv/bin/python /home/miran045/reine097/projects/SynthSeg/SynthSeg/dcan/img_processing/chirality_correction/chirality_correction_for_folds.py $1 $2
EOT
