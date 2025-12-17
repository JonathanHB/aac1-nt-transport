#!/bin/bash
#$ -S /bin/bash         #-- the shell for the job
#$ -q gpu.q             #-- use the gpu queue
#$ -j y                 #-- tell the system that the STDERR and STDOUT should be joined
#$ -cwd                 #-- tell the job that it should start in your working directory
#$ -l mem_free=2G       #-- submits on nodes with enough free memory
#$ -l h_rt=2:00:00      #-- runtime limit - max 2 weeks == 336 hours
##$ -l hostname=cc-idgpu[4] #-- request the RTX 2080 Ti nodes
#$ -N mtdtest
##$ -pe mpi_onehost 4   # we want 4 mpi nodes on 1 gpu
#$ -t 1-100             # number to run at a time (the total number in the job array)
#$ -tc 1                # how many to run at a time (the number of parallel simulations at any given time)
#$ -l hostname=!('qb3-atgpu13'|'qb3-atgpu23'|'qb3-idgpu11'|'qb3-idgpu12'|'qb3-idgpu13'|'qb3-idgpu14'|'qb3-idgpu15'|'qb3-iogpu4'|'msg-iogpu3'|'msg-iogpu6'|'msg-iogpu7') #--don't run on this gpu, which causes jobs to crash because it lacks a gpu with id 0

#warning: commented out lines beginning in "#$" will result in 
#a 'qsub: unknown option' error upon job submission

date
hostname

## GPU/CPU stuff
GMX_CPUS=3
export CUDA_VISIBLE_DEVICES=$SGE_GPU
export OMP_NUM_THREADS=8
echo $CUDA_VISIBLE_DEVICES
echo $OMP_NUM_THREADS


## Get software
module load mpi
module load Sali
module load cuda/10.0.130


GMX=/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi
#/wynton/home/grabe/jborowsky/gromacs/plumed-gromacs/gromacs-2024.4/build/bin/gmx
#/wynton/home/grabe/jborowsky/gromacs/gromacs-2024.4/build/bin/gmx
#alias gmx=$GMX

#for full gpu offloading
export GMX_GPU_DD_COMMS=true
export GMX_GPU_PME_PP_COMMS=true
export GMX_FORCE_UPDATE_DEFAULT_GPU=true

export CUDA_VISIBLE_DEVICES=$SGE_GPU


#run simulation
$GMX mdrun -s ../../inputs/aac1_atp_hmr_4fs_notrr.tpr -cpi state.cpt -x -cpo -nsteps 1250000000 -noappend -nb gpu -pme gpu -bonded gpu -plumed plumed.dat

#-nb gpu -pme gpu -bonded gpu -update gpu

## End-of-job summary, if running as a job
[[ -n "$JOB_ID" ]] && qstat -j "$JOB_ID"  # This is useful for debugging and usage purposes,
                                          # e.g. "did my job exceed its memory request?"
