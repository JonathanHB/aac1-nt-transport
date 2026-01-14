
echo "Enter password:"
read -s PASSWORD

#two_digits_zero_fill ()
#{
#    # print the number as a string with a leading zero
#    printf '%02d' "$1"
#}

runnum=$1

#cd run$runnum

cd run_c

for i in {0..7};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run$runnum/run_c/$i/COLVAR COLVAR.$i
done

cd ../run_m

for i in {0..7};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run$runnum/run_m/$i/COLVAR COLVAR.$i
done
cd ..
