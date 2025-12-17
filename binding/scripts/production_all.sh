runfolder=rotated-cavity-atp

for i in {1..8};
do
	DIRECTORY=run$(printf '%02d' "$i")-aac1-c-atp
	if [ ! -d "$DIRECTORY" ]; then
		mkdir $DIRECTORY
	fi

	if [ -f "../../equilibration/${runfolder}/${DIRECTORY}/run/all_dynamics_segs_mol.xtc" ] && ! [ "$(ls -A $DIRECTORY)" ]; then
		cd $DIRECTORY
		qsub ../../scripts/production_wrapper.sh ../../../equilibration/${runfolder}/${DIRECTORY}
		cd ..
	fi
done

for i in {9..16};
do
	DIRECTORY=run$(printf '%02d' "$i")-aac1-m-atp
	if [ ! -d "$DIRECTORY" ]; then
		mkdir $DIRECTORY
	fi

	if [ -f "../../equilibration/${runfolder}/${DIRECTORY}/run/all_dynamics_segs_mol.xtc" ] && ! [ "$(ls -A $DIRECTORY)" ]; then
		cd $DIRECTORY
		qsub ../../scripts/production_wrapper.sh ../../../equilibration/${runfolder}/${DIRECTORY}
		cd ..
	fi
done
