#imports are not actually needed, ignore the linter error message for the cmd library
import os
#import sys
segnum = 3 #int(sys.argv[1])

for i in range(0,8):
    fn = f"c_run{str(i).zfill(2)}_mtd_seg_{str(segnum).zfill(2)}_centered"

    filepath = f"/home/jonathan/Documents/grabelab/aac1-nt-transport/metadynamics/run2/run_c/{fn}.gro"
    if os.path.exists(filepath):
        cmd.load(filepath)
        util.cbag(fn)
        if i > 1:
            cmd.align(fn, f"c_run01_mtd_seg_{str(segnum).zfill(2)}_centered and poly")

for i in range(0,8):
    fn = f"m_run{str(i).zfill(2)}_mtd_seg_{str(segnum).zfill(2)}_centered"

    filepath = f"/home/jonathan/Documents/grabelab/aac1-nt-transport/metadynamics/run2/run_m/{fn}.gro"
    if os.path.exists(filepath):
        cmd.load(filepath)
        util.cbac(fn)
        if i > 1:
            cmd.align(fn, f"m_run01_mtd_seg_{str(segnum).zfill(2)}_centered and poly")

cmd.hide("everything")
cmd.show("cart")
cmd.show("sticks", "(poly or resn ATP) and not elem H")
util.cbam("resn ATP")
cmd.show("spheres", "resn POT or resn CLA")
cmd.color("yellow", "resn CLA")


