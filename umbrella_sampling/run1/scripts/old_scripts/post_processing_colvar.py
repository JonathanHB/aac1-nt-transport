import os
#calculate colvar from existing trajectories

nwalkers = 32

os.chdir("run_c")

for wi in range(nwalkers):
	if os.path.exists(f"{wi}"):
		os.chdir(f"{wi}")
		print(wi)
		if not os.path.exists("colvars"):
			os.mkdir("colvars")
        
		os.chdir("colvars")
        
		for parti in range(1,100):

			if parti == 1:
				xtcfile = f"../mtd_seg_01.xtc"
			else:
				xtcfile = f"../mtd_seg_01.part{parti:04d}.xtc"
			if os.path.exists(xtcfile):
				os.system(f'sed "s/@part@/{parti:04d}/" ../../../inputs/plumed/plumed_postprocessing.dat > plumed_{parti:04d}.dat')

				os.system(f"plumed driver --mf_xtc {xtcfile} --plumed plumed_{parti:04d}.dat")
			else:
				break
		os.chdir("../..")
            
        

