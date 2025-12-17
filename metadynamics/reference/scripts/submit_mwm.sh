nwalkers=$1

for((i=0;i<$nwalkers;i++)) ; do
mkdir $i
#cp ../inputs/aac1_atp_hmr_4fs_notrr.tpr $i/
sed "s/@id@/$i/" ../inputs/plumed_mwm.dat > $i/plumed_a.dat
sed "s/@nw@/$nwalkers/" $i/plumed_a.dat > $i/plumed.dat
done

for((i=0;i<$nwalkers;i++)) ; do
cd $i
qsub ../../scripts/run_job_array_production_rrm.sh
cd ../
done
