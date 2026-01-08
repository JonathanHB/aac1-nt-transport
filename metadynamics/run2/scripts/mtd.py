#Jonathan Borowsky
#Grabe lab
#12/5/25

#This script is intended to run mtd MD simulations in equal-sized segments which may be longer than the wynton job limit.

#The outline of the script is as follows:
# if there is no checkpoint file and no existing trajectories, or if the previous simulation segment is finished (i.e. if there is a gro file matching the latest xtc), 
#     make a tpr file and start a new segment
# if there is a checkpoint and an incomplete existing trajectory segment:
#     determine the segment number of the most recent trajectory file
#     if there is no gro file for that segment number (i.e. if the current segment is incomplete), run a simulation appending to the current trajectory
# if there is a checkpoint but no existing trajectories or vice versa, exit with an error

import time
t1 = time.time()

import sys
import os

def gmxrun(command):
    header = '''
        module load mpi
        module load Sali
        module load cuda/10.0.130
        GMX=/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi
        export GMX_GPU_DD_COMMS=true
        export GMX_GPU_PME_PP_COMMS=true
        export GMX_FORCE_UPDATE_DEFAULT_GPU=true
        export GMX_NO_QUOTES=True
        export OMP_NUM_THREADS=8
        export CUDA_VISIBLE_DEVICES=$SGE_GPU
        '''

    return os.system(f"{header}\n{command}")


#GMX="/wynton/home/grabe/jborowsky/gromacs/plumed_gmx_122825/gromacs/bin/gmx_mpi"
#GMX="/wynton/home/grabe/jborowsky/gromacs/plumed_gmx_122325/gromacs/gromacs-2025.0/build/bin/gmx_mpi"

## TODO: fix discrepancy between file path and gromacs version
#GMX="/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi"

#mdp = "mdp_hmr_4fs_debug_short.mdp"
mdp_tpr = "mdp_hmr_4fs"

ndigits = 2

#WARNING: when using plumed (and possibly in general) this results in failure to save the .cpt file properly
#it is not clear why but similar issues have been reported
#https://gitlab.com/gromacs/gromacs/-/issues/1942
#https://www.mail-archive.com/gromacs.org_gmx-users@maillist.sys.kth.se/msg18550.html

#normally this loop never gets past the first iteration, but if a round finishes it can use the rest of the node time to start the next round
# for round in range(1):

all_files = os.listdir()
xtc_files = [f for f in all_files if f[-4:] == ".xtc"]
gro_files = [f for f in all_files if f[-4:] == ".gro"]

if len(xtc_files) > 0:
    xtc_segnum = max([int(f[-4-ndigits:-4]) for f in xtc_files])
elif len(xtc_files) == 0:
    xtc_segnum = 0
else:
    print(f"error: negative list length of {len(xtc_files)}; something has gone horribly wrong.")
    sys.exit(0)

if len(gro_files) > 0:
    gro_segnum = max([int(f[-4-ndigits:-4]) for f in gro_files])
elif len(gro_files) == 0:
    gro_segnum = 0
else:
    print(f"error: negative list length of {len(gro_files)}; something has gone horribly wrong.")
    sys.exit(0)


#if there is no checkpoint file and no existing trajectories, start a simulation with segment number 1 
# make a tpr using the configuration in the last equilibration file
if not os.path.exists("state.cpt"):

    gmxrun(f"$GMX grompp -f ../../inputs/mdp/{mdp_tpr}.mdp -o {mdp_tpr}_01.tpr -c {sys.argv[1]}/seg_06.gro -p {sys.argv[1]}/topol.top -n {sys.argv[1]}/index.ndx")
    
    t2 = time.time()
    t_left = 2-(t2 - t1)/3600  #2 hours minus time already used, in hours

    #TODO can we make this one command run after the if statements and set the parameters beforehand? be careful with the -cpi flag here
    gmxrun(f"$GMX mdrun -s {mdp_tpr}_01.tpr -cpo -x mtd_seg_01.xtc -e ener_01.edr -g md.log_01.log -c mtd_seg_01.gro -nb gpu -pme gpu -bonded gpu -maxh {t_left} -plumed plumed.dat")


#start new segment if current one is complete
elif xtc_segnum == gro_segnum:

    next_ind = str(gro_segnum+1).zfill(ndigits)

    gmxrun(f"$GMX grompp -f ../../inputs/mdp/{mdp_tpr}.mdp -o {mdp_tpr}_{next_ind}.tpr -c mtd_seg_{str(gro_segnum).zfill(ndigits)}.gro -p {sys.argv[1]}/topol.top -n {sys.argv[1]}/index.ndx")
    
    t2 = time.time()
    t_left = 2-(t2 - t1)/3600  #2 hours minus time already used, in hours

    gmxrun(f"$GMX mdrun -s {mdp_tpr}_{next_ind}.tpr -cpo -x mtd_seg_{next_ind}.xtc -e ener_{next_ind}.edr -g md.log_{next_ind}.log -c mtd_seg_{next_ind}.gro -nb gpu -pme gpu -bonded gpu -maxh {t_left} -plumed plumed.dat")


#if there is an incomplete segment, resume from checkpoint file and append it
elif xtc_segnum == gro_segnum+1:

    ind = str(xtc_segnum).zfill(ndigits)

    t2 = time.time()
    t_left = 2-(t2 - t1)/3600  #2 hours minus time already used, in hours

    gmxrun(f"$GMX mdrun -s {mdp_tpr}_{ind}.tpr -cpi state.cpt -cpo -x mtd_seg_{ind}.xtc -e ener_{ind}.edr -g md.log_{ind}.log -c mtd_seg_{ind}.gro -append -nb gpu -pme gpu -bonded gpu -maxh {t_left} -plumed plumed.dat")


#    break

#     #start new segment if current one is complete
#     elif gro_segnum == xtc_segnum:
#         os.system(f"export GMX_NO_QUOTES=True; export CUDA_VISIBLE_DEVICES=$SGE_GPU; \
#                   {GMX} mdrun -s {tpr} -cpi state.cpt -cpo -x mtd_seg_{str(xtc_segnum+1).zfill(ndigits)}.xtc -c mtd_seg_{str(xtc_segnum+1).zfill(ndigits)}.gro -noappend -nb gpu -pme gpu -bonded gpu -update gpu")

#     #exit if run numbers imply a previous error
#     else:
#         print("error: inconsistent numbering of most recent segments:")
#         print(f"most recent gro file: {gro_segnum}")
#         print(f"most recent xtc file: {xtc_segnum}")
#         #terminate parent task and exit
#         os.system(f"qdel {sys.argv[2]}")
#         sys.exit(0)

# #if there is a checkpoint but no existing trajectories or vice versa, exit with an error
# else:
#     print("error: inconsistent file existence pattern:")
#     print(f"state.cpt found: {os.path.exists('state.cpt')}")
#     print(f"gro files found: {gro_files}")
#     print(f"xtc files found: {xtc_files}")
#     #terminate parent task and exit
#     os.system(f"qdel {sys.argv[2]}")
#     sys.exit(0)

# if there is no checkpoint file and no existing trajectories, start a simulation with segment number 1
#     if there is a checkpoint but no existing trajectories or vice versa, exit with an error
# if there is a checkpoint and an existing trajectory:
#     determine the segment number of the most recent trajectory file
#     if there is no gro file for that segment number (i.e. if the current segment is incomplete), run a simulation appending to the current trajectory
#     if there is a gro file (written at the end of a completed segment), start the next segment of the simulation
