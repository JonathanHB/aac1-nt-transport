
echo "Enter password:"
read -s PASSWORD

#two_digits_zero_fill ()
#{
#    # print the number as a string with a leading zero
#    printf '%02d' "$1"
#}

echo "copying from run $1"

nwalkers=32

cd run_c

for ((i=0; i<$nwalkers; i++))
do
	if [ ! -d "$i" ]; then
		mkdir $i
	fi

	# for ((j=0; j<10; j++))
	# do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/relaxation/run$1/run_c/$i/colvars/COLVAR.* $i
	# done

done

# sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run$1/run_c/summed_hills/fes-$2.dat summed_hills/fes-$2.dat

# cd ../run_m

# for i in {0..7};
# do
# 	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run$1/run_m/$i/COLVAR COLVAR.$i
# done

# sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run$1/run_m/summed_hills/fes-$2.dat summed_hills/fes-$2.dat

cd ..
