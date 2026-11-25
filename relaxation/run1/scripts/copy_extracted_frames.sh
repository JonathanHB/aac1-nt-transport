
echo "Enter password:"
read -s PASSWORD

#two_digits_zero_fill ()
#{
#    # print the number as a string with a leading zero
#    printf '%02d' "$1"
#}

runnum=4
segnum=1 #$1

cd run_c

sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run4/run_c/1/mdp_hmr_4fs_01.tpr .
for i in {0..32};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/relaxation/run1/frame_extraction/frame_$i.gro .
	echo 1 0 | gmx trjconv -f frame_$i.gro -s mdp_hmr_4fs_01.tpr -pbc mol -center -o frame_${i}_centered.gro
done