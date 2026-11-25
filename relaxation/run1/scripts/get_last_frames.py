import os
import sys

gmx="/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi"

nwalkers = 32

os.chdir("run_c")

for wi in range(nwalkers):
	if os.path.exists(f"{wi}"):
		os.chdir(f"{wi}")
		print(wi)
		if not os.path.exists(f"last_frames_{sys.argv[1]}"):
			os.mkdir(f"last_frames_{sys.argv[1]}")
        
		os.chdir(f"last_frames_{sys.argv[1]}")
        
		for parti_ in range(100):
			parti = 101 - parti_
			if parti == 1:
				xtcfile = f"../mtd_seg_01.xtc"
			else:
				xtcfile = f"../mtd_seg_01.part{parti:04d}.xtc"
			if os.path.exists(xtcfile):
				os.system(f"echo 1 0 | {gmx} trjconv -f {xtcfile} -s ../mdp_hmr_4fs_01.tpr -center -pbc mol -o {wi}_{sys.argv[1]}.gro -dump -1")
				#os.system(f"echo 1 1 0 | {gmx} trjconv -f mtd_seg_01_centered_mol.all.xtc -s ../mdp_hmr_4fs_01.tpr -center -fit rot+trans -o mtd_seg_01_aligned.all.c.{wi}.xtc")
				#os.system(f"plumed driver --mf_xtc {xtcfile} --plumed plumed_{parti:04d}.dat")

				break

		os.chdir("../..")


# nwalkers=32
# out_dir=last_frames_$1
# gmx=/wynton/home/grabe/jborowsky/gromacs/gmx_2024.4_plumed_mpi/gromacs/gromacs-2024.3/build/bin/gmx_mpi

# cd run_c

# for ((i=0; i<$nwalkers; i++))
# do
# 	if [ -d "$i" ]; then
# 		cd $i
# 		if [ ! -d "$out_dir" ]; then
# 			mkdir $out_dir
# 		fi
# 		cd $out_dir
# 			#$gmx trjcat -f ../mtd_seg_01.part00*.xtc -o mtd_seg_01.all.xtc
# 			echo 1 0 | $gmx trjconv -f mtd_seg_01.all.xtc -s ../mdp_hmr_4fs_01.tpr -center -pbc mol -o mtd_seg_01_centered_mol.all.xtc -skip 4
# 			echo 1 1 0 | $gmx trjconv -f mtd_seg_01_centered_mol.all.xtc -s ../mdp_hmr_4fs_01.tpr -center -fit rot+trans -o mtd_seg_01_aligned.all.c.$i.xtc
		
# 		cd ../..
# 	fi
# done

# cd ../run_m

# for ((i=0; i<$nwalkers; i++))
# do
# 	if [ -d "$i" ]; then
# 		cd $i
# 		if [ ! -d "$out_dir" ]; then
# 			mkdir $out_dir
# 		fi
# 		cd $out_dir
# 			$gmx trjcat -f ../mtd_seg_01.part00*.xtc -o mtd_seg_01.all.xtc
# 			echo 1 0 | $gmx trjconv -f mtd_seg_01.all.xtc -s ../mdp_hmr_4fs_01.tpr -center -pbc mol -o mtd_seg_01_centered_mol.all.xtc -skip 4
# 			echo 1 1 0 | $gmx trjconv -f mtd_seg_01_centered_mol.all.xtc -s ../mdp_hmr_4fs_01.tpr -center -fit rot+trans -o mtd_seg_01_aligned.all.m.$i.xtc
		
# 		cd ../..
# 	fi
# done

# for ((i=0; i<$nwalkers; i++))
# do
# 	DIRECTORY=$i #run$(printf '%02d' "$i")-aac1-m-atp
# 	if [ ! -d "$DIRECTORY" ]; then
# 		mkdir $DIRECTORY
# 	fi

# 	#if [ -f "../../equilibration/${runfolder}/${DIRECTORY}/run/all_dynamics_segs_mol.xtc" ] && ! [ "$(ls -A $DIRECTORY)" ]; then
# 	cd $DIRECTORY

# 	sed "s/@id@/$i/" ../../inputs/plumed/plumed_mwm.dat > plumed_a.dat
# 	sed "s/@nw@/$nwalkers/" plumed_a.dat > plumed.dat

# 	qsub ../../scripts/mtd_wrapper.sh ../../inputs/gromacs_m $nwalkers #scripts/production_wrapper.sh ../../../equilibration/${runfolder}/${DIRECTORY}
# 	cd ..
# 	#fi
# done

# cd ..
