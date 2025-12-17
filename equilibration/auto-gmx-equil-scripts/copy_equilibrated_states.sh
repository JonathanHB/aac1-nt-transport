
echo "Enter password:"
read -s PASSWORD

#two_digits_zero_fill ()
#{
#    # print the number as a string with a leading zero
#    printf '%02d' "$1"
#}

for i in {1..8};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/equilibration/rotated-cavity-atp/run0$i-aac1-c-atp/run/seg_0023.gro run0$i-aac1-c-atp-seg_0023.gro
done

for i in {9..16};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/equilibration/rotated-cavity-atp/run$(printf '%02d' "$i")-aac1-m-atp/run/seg_0023.gro run$(printf '%02d' "$i")-aac1-m-atp-seg_0023.gro
done
