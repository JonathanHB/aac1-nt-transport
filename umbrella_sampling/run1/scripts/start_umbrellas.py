#Jonathan Borowsky
#01/25/26
#Grabe lab

import os
import numpy as np

n_windows = 24
wincenters = np.load("scripts/window_centers.npy")

os.chdir("run_c")

for w in range(n_windows):
    if os.path.exists(f"../frame_extraction/frame_{w}.gro"):
        #print(w)
        if not os.path.exists(str(w)):
            os.mkdir(str(w))

        os.chdir(str(w))

        #set restraint center position to correct value in plumed.dat file and copy it here
        os.system(f'sed "s/@x0@/{wincenters[w]}/" ../../inputs/plumed/plumed_umbrellas.dat > plumed.dat')
        #start simulation
        os.system(f'qsub ../../scripts/submit_md.sh ../../inputs/gromacs_c {n_windows} {w}')
        
        os.chdir("..")
