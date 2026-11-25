import numpy as np
import os

gmx="/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi"

times = np.load("times_spaced.npy")
x = 0
for t in times:
    print(f"{t} ps")
    os.system(f"echo 0 | {gmx} trjconv -f mtd_seg_01.all.xtc -s ../mdp_hmr_4fs_01.tpr -o frame_{x}.gro -dump {int(t)}")

    x += 1