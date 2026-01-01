#!/bin/bash
#$ -S /bin/bash         #-- the shell for the job
#$ -q gpu.q             #-- use the gpu queue
#$ -j y                 #-- tell the system that the STDERR and STDOUT should be joined
#$ -cwd                 #-- tell the job that it should start in your working directory
#$ -l mem_free=2G       #-- submits on nodes with enough free memory
#$ -l h_rt=2:00:00      #-- runtime limit - max 2 weeks == 336 hours #I believe it is currently set to 2 hours
##$ -l hostname=cc-idgpu[4] #-- request the RTX 2080 Ti nodes
#$ -N eq
##$ -pe mpi_onehost 4     #we want 4 mpi nodes on 1 gpu
#$ -t 1-100              # number to run at a time (the total number in the job array)
#$ -tc 1              # how many to run at a time (the number of parallel simulations at any given time)
#$ -l hostname=!('qb3-atgpu13'|'qb3-atgpu23'|'qb3-idgpu11'|'qb3-idgpu12'|'qb3-idgpu13'|'qb3-idgpu14'|'qb3-idgpu15'|'qb3-iogpu4'|'msg-iogpu2'|'msg-iogpu3'|'msg-iogpu6'|'msg-iogpu7') #--don't run on this gpu, which causes jobs to crash because it lacks a gpu with id 0
# #$ -l hostname=!(‘qb3-atgpu*‘|'qb3-atgpu**‘)

date
hostname

## GPU/CPU stuff
#GMX_CPUS=3
export CUDA_VISIBLE_DEVICES=$SGE_GPU
export OMP_NUM_THREADS=8
echo $CUDA_VISIBLE_DEVICES
echo $OMP_NUM_THREADS


## Get software
module load mpi
module load Sali
module load cuda/10.0.130


# GMX_VER=2020.6
# GMX=/wynton/home/grabe/shared/gromacs/gromacs-${GMX_VER}_CUDA10_SSE4/bin/gmx
# alias gmx=$GMX
# TODO: fix discrepancy between file path and gromacs version
#GMX=/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi

#for full gpu offloading
export GMX_GPU_DD_COMMS=true
export GMX_GPU_PME_PP_COMMS=true
#export GMX_FORCE_UPDATE_DEFAULT_GPU=true

#echo $1

#these supply python even though no WE simulations are being run
module load CBI miniconda3/4.12.0-py39
conda activate westpa-2.0

python ../../scripts/mtd.py $1 #$2 #$JOB_ID

# found_cpt_file=false

# for file in *; do
#     if [[ -f "$file" && "$file" == *.cpt ]]; then
#         found_cpt_file=true
#         break # Exit the loop as soon as a .cpt file is found
#     fi
# done

# if ! $found_cpt_file; then
#     echo "No file ending with .cpt found in the current directory."
#     $GMX mdrun -s plain_binding_hmr_4fs.tpr -cpo -x plain_seg_$(printf '%02d' "$SGE_TASK_ID").xtc -nb gpu -pme gpu -bonded gpu -update gpu
# else
#     echo "At least one file ending with .sh was found in the current directory."
#     $GMX mdrun -s plain_binding_hmr_4fs.tpr -cpi state.cpt -cpo -x plain_seg_$(printf '%02d' "$SGE_TASK_ID").xtc -append -nb gpu -pme gpu -bonded gpu -update gpu
# fi

# $GMX mdrun -s plain_binding_hmr_4fs.tpr -cpi state.cpt -cpo -x plain_seg_$(printf '%02d' "$SGE_TASK_ID").xtc -append -nb gpu -pme gpu -bonded gpu -update gpu

#python ../../auto-gmx-equil-scripts/rrm-equilibration.py $SGE_TASK_ID $JOB_ID $1

## End-of-job summary, if running as a job
[[ -n "$JOB_ID" ]] && qstat -j "$JOB_ID"  # This is useful for debugging and usage purposes,
                                          # e.g. "did my job exceed its memory request?"
