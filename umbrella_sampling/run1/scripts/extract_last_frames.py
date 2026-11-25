import os
import sys

gmx="/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi"

nwalkers = 24

os.chdir("run_c")

for wi in range(nwalkers):
	if os.path.exists(f"{wi}"):
		os.chdir(f"{wi}")
		if not os.path.exists(f"last_frames_{sys.argv[1]}"):
			os.mkdir(f"last_frames_{sys.argv[1]}")
        
		os.chdir(f"last_frames_{sys.argv[1]}")
        
		for parti_ in range(100):
			parti = 101 - parti_
			if parti == 1:
				xtcfile = f"../mtd_seg_01.xtc" #the 'mtd' part is at this point a misnomer
			else:
				xtcfile = f"../mtd_seg_01.part{parti:04d}.xtc"
			if os.path.exists(xtcfile):
				os.system(f"echo 1 0 | {gmx} trjconv -f {xtcfile} -s ../mdp_hmr_4fs_01.tpr -center -pbc mol -o {wi}_{sys.argv[1]}.gro -dump -1")
				#os.system(f"echo 1 1 0 | {gmx} trjconv -f mtd_seg_01_centered_mol.all.xtc -s ../mdp_hmr_4fs_01.tpr -center -fit rot+trans -o mtd_seg_01_aligned.all.c.{wi}.xtc")
				#os.system(f"plumed driver --mf_xtc {xtcfile} --plumed plumed_{parti:04d}.dat")

				break

		os.chdir("../..")