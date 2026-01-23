import plumed
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os       


colvar=plumed.read_as_pandas("COLVAR")

#get regularly spaced points that are at least 0.03 nm apart in both dimensions
time = list(colvar.time)

delta = list(colvar.pc_f1b)
pc_c = list(colvar.pc_fc)
pc_m = list(colvar.pc_fm)

sigma = [i+j for i,j in zip(pc_c,pc_m)]

coords = []
times = []

thresh = 0.03

for t, (d,s) in enumerate(zip(delta, sigma)):
    farenough = True
    for c in coords:
        if abs(d - c[0]) < thresh and abs(s - c[1]) < thresh:
            farenough = False
            break

    if farenough or t == len(time)-1:
        times.append(time[t])
        print(f"{time[t]} ps")
        coords.append((d,s))

        os.system(f"gmx trjconv -f mtd_seg_01.all.xtc -s ../mdp_hmr_4fs_01.tpr -o frame_{time[t]:.1f}ns.pdb -dump {time[t]:.1f}")

print(f"found {len(coords)} points")
#plt.scatter([c[0] for c in coords], [c[1] for c in coords], color = "blue", s=2, zorder = 10000)

np.save("times_spaced.npy", times)