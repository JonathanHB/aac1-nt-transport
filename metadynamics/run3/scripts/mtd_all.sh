runfolder=rotated-cavity-atp

nwalkers=8
#max_dir_ind=$(($nwalkers-1))


cd run_c

for ((i=0; i<$nwalkers; i++))
do
	DIRECTORY=$i #run$(printf '%02d' "$i")-aac1-c-atp
	if [ ! -d "$DIRECTORY" ]; then
		mkdir $DIRECTORY
	fi

	#if [ -f "../../inputs/gromacs_c/${DIRECTORY}/run/all_dynamics_segs_mol.xtc" ] && ! [ "$(ls -A $DIRECTORY)" ]; then
	cd $DIRECTORY

	sed "s/@id@/$i/" ../../inputs/plumed/plumed_mwm.dat > plumed_a.dat
	sed "s/@nw@/$nwalkers/" plumed_a.dat > plumed.dat

	qsub ../../scripts/mtd_wrapper.sh ../../inputs/gromacs_c #../../../equilibration/${runfolder}/${DIRECTORY}
	cd ..
	#fi
done

cd ../run_m

for ((i=0; i<$nwalkers; i++))
do
	DIRECTORY=$i #run$(printf '%02d' "$i")-aac1-m-atp
	if [ ! -d "$DIRECTORY" ]; then
		mkdir $DIRECTORY
	fi

	#if [ -f "../../equilibration/${runfolder}/${DIRECTORY}/run/all_dynamics_segs_mol.xtc" ] && ! [ "$(ls -A $DIRECTORY)" ]; then
	cd $DIRECTORY

	sed "s/@id@/$i/" ../../inputs/plumed/plumed_mwm.dat > plumed_a.dat
	sed "s/@nw@/$nwalkers/" plumed_a.dat > plumed.dat

	qsub ../../scripts/mtd_wrapper.sh ../../inputs/gromacs_m #scripts/production_wrapper.sh ../../../equilibration/${runfolder}/${DIRECTORY}
	cd ..
	#fi
done

cd ..
