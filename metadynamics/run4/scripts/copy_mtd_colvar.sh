
echo "Enter password:"
read -s PASSWORD

#two_digits_zero_fill ()
#{
#    # print the number as a string with a leading zero
#    printf '%02d' "$1"
#}

#segnum=$1

echo "copying from run $1"

cd run_c

for i in {0..7};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run$1/run_c/$i/COLVAR COLVAR.$i
done

cd ../run_m

for i in {0..7};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run$1/run_m/$i/COLVAR COLVAR.$i
done
cd ..
