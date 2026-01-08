import os
import sys

n_walkers = 8
date = "010826"

#hills_string_1 = ",".join([f'HILLS.{i}' for i in range(n_walkers)])#+",bck.0.HILLS.0,bck.0.HILLS.1"
hills_string_1 = ",".join([f'bck.0.HILLS.{i}' for i in range(n_walkers)])
print(hills_string_1)
#print(hills_string_2)

header = """
    module load mpi
    module load Sali
    module load cuda/10.0.130
    """

plumed_command = f"plumed sum_hills --hills {hills_string_1} --mintozero --outfile summed_hills/fes-from-bck-{date}.dat"

os.system(f"{header}\n{plumed_command}")
