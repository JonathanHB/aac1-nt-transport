import numpy as np
import os

gmx="/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi"

input = "/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run4/run_c/1"

times = np.load("../scripts/window_init_frame_times.npy")
x = 0
for t in times:
    print(f"{t} ps")
    os.system(f"echo 0 | {gmx} trjconv -f {input}/frame_extraction/mtd_seg_01.all.xtc -s {input}/mdp_hmr_4fs_01.tpr -o frame_{x}.gro -dump {int(t)}")
    os.system(f"echo 1 0 | {gmx} trjconv -f {input}/frame_extraction/mtd_seg_01.all.xtc -s {input}/mdp_hmr_4fs_01.tpr -o centered/frame_{x}_cm.gro -dump {int(t)} -pbc mol -center")

    x += 1