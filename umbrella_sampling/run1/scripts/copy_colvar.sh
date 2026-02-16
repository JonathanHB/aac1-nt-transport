
echo "Enter password:"
read -s PASSWORD

echo "copying from run $1"

nsimulations=24

cd run_c

for ((i=0; i<$nsimulations; i++))
do
	if [ ! -d "$i" ]; then
		mkdir $i
	fi

	sshpass -p "$PASSWORD" scp jborowsky@dt1.wynton.ucsf.edu:/wynton/home/grabe/jborowsky/aac1-nt-transport/umbrella_sampling/run$1/run_c/$i/COLVAR COLVAR.$i

done