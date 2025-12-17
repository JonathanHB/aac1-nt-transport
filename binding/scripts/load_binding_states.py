#imports are not actually needed, ignore the linter error message for the cmd library
import os
#import sys
segnum = 3 #int(sys.argv[1])

for i in range(1,9):
    filepath = f"/home/jonathan/Documents/grabelab/aac1-nt-transport/binding/rotated-cavity-atp/run{str(i).zfill(2)}-aac1-c-atp-seg_{str(segnum).zfill(2)}.gro"
    if os.path.exists(filepath):
        cmd.load(filepath)
        util.cbag(f"run{str(i).zfill(2)}-aac1-c-atp-seg_{str(segnum).zfill(2)}")
        if i > 1:
            cmd.align(f"run{str(i).zfill(2)}-aac1-c-atp-seg_{str(segnum).zfill(2)}", f"run01-aac1-c-atp-seg_{str(segnum).zfill(2)} and poly")

for i in range(9,17):
    filepath = f"/home/jonathan/Documents/grabelab/aac1-nt-transport/binding/rotated-cavity-atp/run{str(i).zfill(2)}-aac1-m-atp-seg_{str(segnum).zfill(2)}.gro"
    if os.path.exists(filepath):
        cmd.load(filepath)
        util.cbac(f"run{str(i).zfill(2)}-aac1-m-atp-seg_{str(segnum).zfill(2)}")
        if i == 9:
            cmd.align(f"run{str(i).zfill(2)}-aac1-m-atp-seg_{str(segnum).zfill(2)}", f"run01-aac1-c-atp-seg_{str(segnum).zfill(2)} and poly")
        if i > 9:
            cmd.align(f"run{str(i).zfill(2)}-aac1-m-atp-seg_{str(segnum).zfill(2)}", f"run09-aac1-m-atp-seg_{str(segnum).zfill(2)} and poly")

cmd.hide("everything")
cmd.show("cart")
cmd.show("sticks", "(poly or resn ATP) and not elem H")
util.cbam("resn ATP")
cmd.show("spheres", "resn POT or resn CLA")
cmd.color("yellow", "resn CLA")


