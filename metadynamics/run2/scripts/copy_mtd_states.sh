
echo "Enter password:"
read -s PASSWORD

#two_digits_zero_fill ()
#{
#    # print the number as a string with a leading zero
#    printf '%02d' "$1"
#}

segnum=$1

cd run_c

sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run2/run_c/0/mdp_hmr_4fs_01.tpr mdp_hmr_4fs_01.tpr

for i in {0..7};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run2/run_c/$i/mtd_seg_$(printf '%02d' "$segnum").gro   c_run$(printf '%02d' "$i")_mtd_seg_$(printf '%02d' "$segnum").gro
	echo 1 0 | gmx trjconv -f c_run$(printf '%02d' "$i")_mtd_seg_$(printf '%02d' "$segnum").gro -s mdp_hmr_4fs_01.tpr -pbc mol -center -o c_run$(printf '%02d' "$i")_mtd_seg_$(printf '%02d' "$segnum")_centered.gro
done

cd ../run_m

sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run2/run_m/0/mdp_hmr_4fs_01.tpr mdp_hmr_4fs_01.tpr

for i in {0..7};
do
	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/metadynamics/run2/run_m/$i/mtd_seg_$(printf '%02d' "$segnum").gro   m_run$(printf '%02d' "$i")_mtd_seg_$(printf '%02d' "$segnum").gro
	echo 1 0 | gmx trjconv -f m_run$(printf '%02d' "$i")_mtd_seg_$(printf '%02d' "$segnum").gro -s mdp_hmr_4fs_01.tpr -pbc mol -center -o m_run$(printf '%02d' "$i")_mtd_seg_$(printf '%02d' "$segnum")_centered.gro
done
cd ..
