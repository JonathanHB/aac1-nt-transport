#imports are not actually needed, ignore the linter error message for the cmd library

fn = "rotated-cavity-atp"

for i in range(1,9):
    path = f"/home/jonathan/Documents/grabelab/aac1-nt-transport/equilibration/{fn}/run{str(i).zfill(2)}-aac1-c-atp-seg_0023.gro"
    if os.path.exists(path):
        cmd.load(path)
        if i > 1:
            cmd.align(f"run{str(i).zfill(2)}-aac1-c-atp-seg_0023", "run01-aac1-c-atp-seg_0023 and poly")

for i in range(9,17):
    path = f"/home/jonathan/Documents/grabelab/aac1-nt-transport/equilibration/{fn}/run{str(i).zfill(2)}-aac1-m-atp-seg_0023.gro"
    if os.path.exists(path):
        cmd.load(path)
        if i > 9:
            cmd.align(f"run{str(i).zfill(2)}-aac1-m-atp-seg_0023", "run09-aac1-m-atp-seg_0023 and poly")
