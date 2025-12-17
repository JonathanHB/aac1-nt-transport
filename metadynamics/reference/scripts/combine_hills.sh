#cat HILLS.0 HILLS.1 HILLS.2 HILLS.3 HILLS.4 HILLS.5 HILLS.6 HILLS.7 HILLS.8 | sort -n > HILLS.$1
module load mpi
module load Sali
module load cuda/10.0.130

plumed sum_hills --hills HILLS.0,HILLS.1,HILLS.2,HILLS.3,HILLS.4,HILLS.5,HILLS.6,HILLS.7 --mintozero --outfile summed_hills/fes-$1.dat 
