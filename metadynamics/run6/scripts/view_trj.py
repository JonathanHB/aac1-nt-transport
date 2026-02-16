# state="c"
# replica=3
from pymol import cmd
from pymol import util

print("Loaded view_trj.py, creating command view_trj")

@cmd.extend
def view_trj(instring):

    if instring == "":
        print("Usage: view_trj [initial_state] [replica]")
        return 1
    
    state, replica = instring.split(" ")

    state = state.strip()
    replica = replica.strip()

    print("aaa")
    print(state, replica)

    cmd.delete("all")

    cmd.load(f"inputs/gromacs_{state}/seg_06.gro", "trj")
    cmd.load_traj(f"run_{state}/mtd_seg_01_aligned.all.{state}.{replica}.xtc", "trj")

    cmd.hide("spheres")
    cmd.hide("nb_spheres")
    cmd.hide("lines")
    cmd.hide("sticks", "elem H")
    cmd.show("sticks", "poly and not elem H")

    util.cbag()
    util.cbac("resn POPC+TLCL2")
    util.cbam("resn ATP")

    return 0


#usage: in scripts/
# view_trj c 3
#must be in scripts; can't include path in pymol command
#don't include 'run' or .py with the command