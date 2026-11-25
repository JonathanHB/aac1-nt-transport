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

mdp_tpr = "mdp_hmr_4fs"

ndigits = 2

#WARNING: when using plumed (and possibly in general) the mdrun -maxh flag this results in failure to save the .cpt file properly
#it is not clear why but similar issues have been reported
#https://gitlab.com/gromacs/gromacs/-/issues/1942
#https://www.mail-archive.com/gromacs.org_gmx-users@maillist.sys.kth.se/msg18550.html


all_files = os.listdir()
xtc_files = [f for f in all_files if f[-4:] == ".xtc"]
gro_files = [f for f in all_files if f[-4:] == ".gro"]

xtc_segnum = 1


#if there is no checkpoint file and no existing trajectories, start a simulation with segment number 1 
# make a tpr using the configuration in the last equilibration file
if not os.path.exists("state.cpt"):

    gmxrun(f"$GMX grompp -f ../../inputs/mdp/{mdp_tpr}.mdp -o {mdp_tpr}_01.tpr -c ../../frame_extraction/frame_{sys.argv[3]}.gro -p {sys.argv[1]}/topol.top -n {sys.argv[1]}/index.ndx")
    
    t2 = time.time()
    t_left = 2-(t2 - t1)/3600  #2 hours minus time already used, in hours

    #TODO can we make this one command run after the if statements and set the parameters beforehand? be careful with the -cpi flag here
    gmxrun(f"$GMX mdrun -s {mdp_tpr}_01.tpr -cpo -x mtd_seg_01.xtc -e ener_01.edr -g md.log_01.log -c mtd_seg_01.gro -nb gpu -pme gpu -bonded gpu -maxh {t_left} -plumed plumed.dat")


#end run if simulation segment is complete
elif len(gro_files) > 0: 

    #terminate parent task and exit
    os.system(f"qdel {sys.argv[4]}")
    sys.exit(0)


#if there is an incomplete segment, resume from checkpoint file and append it
elif len(gro_files) == 0: #xtc_segnum == gro_segnum+1:

    #make sure all metadynamics runs have had a first segment to create hills files before trying to read them all in
    #the more sophisticated approach would be to eliminate the association between wynton jobs and md runs and just have this extend whichever run had the least sampling
    #but that would require far more complex code and is probably not worth the trouble at the moment
    #upperdir_files = os.listdir("../")
    #hills_expected = ["HILLS."+str(i) for i in range(int(sys.argv[2]))]
    #for he in hills_expected:
    #    if he not in upperdir_files:
    #        print(f"{he} not found; exiting")
    #        sys.exit(0)

    ind = str(xtc_segnum).zfill(ndigits)

    t2 = time.time()
    t_left = 2-(t2 - t1)/3600  #2 hours minus time already used, in hours

    gmxrun(f"$GMX mdrun -s {mdp_tpr}_{ind}.tpr -cpi state.cpt -cpo -x mtd_seg_{ind}.xtc -e ener_{ind}.edr -g md.log_{ind}.log -c mtd_seg_{ind}.gro -noappend -nb gpu -pme gpu -bonded gpu -maxh {t_left} -plumed plumed.dat")

