#imports are not actually needed, ignore the linter error message for the cmd library
from pymol import cmd
#import time
#from ctypes import util
import os
#import sys

cmd.delete("all")
cmd.fetch("2c3eA")
cmd.fetch("6gciA")
cmd.align("6gciA", "2c3eA")

date = "012726"

for i in range(0,24):
    fn = f"{i}_{date}"
    filepath = f"/home/jonathan/Documents/grabelab/aac1-nt-transport/umbrella_sampling/run1/run_c/{i}/last_frames_{date}/{fn}.gro"

    if os.path.exists(filepath):
        cmd.load(filepath)
        cmd.align(fn, "2c3eA")

cmd.hide("everything")
cmd.show("cart")
cmd.show("sticks", "(poly or resn ATP) and not elem H")
util.cbag()
util.cbam("resn ATP")
#cmd.show("spheres", "resn POT or resn CLA")
#cmd.color("yellow", "resn CLA")