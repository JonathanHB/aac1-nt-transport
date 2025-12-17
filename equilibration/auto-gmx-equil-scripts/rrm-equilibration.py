#Jonathan Borowsky
#051124
#westpa gromacs file copy error handling

import sys
import os
import glob
import time

#lines signalling fatal error requiring restart
#found in the log file in seg_logs/
error_lines = [\
	"Asynchronous H2D copy failed",\
	"Asynchronous D2H copy failed",\
	"The total potential energy is nan, which is not finite.",\
	"Unexpected cudaStreamQuery failure: an illegal memory access was encountered",\
	"Could not register the host memory for page locking for GPU transfers.",\
	"cudaErrorMemoryAllocation: out of memory",\
	"bytes failed: out of memory",\
	"cudaMalloc failure",\
	"cudaStreamSynchronize failed",\
	"Synchronous D2H copy failed",\
	"Synchronous H2D copy failed",\
	"incompatible GPUs: 0. Request only compatible GPUs."]

gmxpath = "/wynton/home/grabe/jborowsky/gromacs/gromacs-2024.4/build/bin/gmx"
#"/wynton/home/grabe/shared/gromacs/gromacs-2020.6_CUDA10_SSE4/bin/gmx"

#-----------------------------------------------------------------------------------------------------
#generate grompp file
#-----------------------------------------------------------------------------------------------------

#get current run number, which is fed in as the argument or two arguments
task_id_number = int(sys.argv[1])

if len(sys.argv) == 3:
	run_number = task_id_number
elif len(sys.argv) == 4:
	run_number = task_id_number+int(sys.argv[3])-1
else:
	print("error: wrong number of arguments")
	sys.exit(0)

#identify the last run with complete output (normally just the last run; ri = 0); then proceed from there
#this could replace the current error-detection code and would require much less code 
#but might be somewhat slower since the error-detection code tries to salvage the current job
#must be run before doing anything with run_number
if run_number != 1:
	for ri in range(999):
		if os.path.exists(f"seg_{str(run_number-ri-1).zfill(4)}.gro"):
			run_number = run_number-ri
			break

#make padded strings for naming files so that they'll stay in order
runstring = str(run_number).zfill(4)
last_runstring = str(run_number-1).zfill(4)

mdpstring = str(run_number).zfill(2)

#get the correct mdp file for the current run
mdpfiles = glob.glob(f"../mdp/seg_{mdpstring}_*.mdp")

#detect when equilibration is done and concatenate/convert trajectories for viewing
if len(mdpfiles) == 0:
	print("No .mdp files detected: assuming that this means equilibration is complete.\
\nWill now concatenate and convert trajectory files")
	
	#this assumes that minimization requires a single segment
	trj_file_list = " ".join([f"seg_{str(i+2).zfill(4)}.xtc" for i in range(run_number-2)])
	gmx_trjcat_command = f"{gmxpath} trjcat -f {trj_file_list} -o all_dynamics_segs.xtc"
	os.system(f"export GMX_NO_QUOTES=True; {gmx_trjcat_command}")

	gmx_trjconv_command = f"echo 1 0 | {gmxpath} trjconv -s seg_0002.tpr -f all_dynamics_segs.xtc -pbc mol -center -o all_dynamics_segs_mol.xtc"
	os.system(f"export GMX_NO_QUOTES=True; {gmx_trjconv_command}")
	
	#terminate parent task and exit
	os.system(f"qdel {sys.argv[2]}")
	sys.exit(0)

elif len(mdpfiles) != 1:
	print(f"error: invalid .mdp file set {mdpfiles} detected, there should be only one .mdp file matching: ../mdp/seg_{mdpstring}_*.mdp")
	sys.exit(0)

#rendered unnecessary by gromacs' existing file backup capabilities
#check for existing files with the current run number and move them out of the way
#existing_run_files = glob.glob(f"seg_{runstring}.*")
#if len(existing_run_files) > 0:
#	if not os.path.exists(f"old_{runstring}"):
#		os.mkdir(f"old_{runstring}")
#       #this line has a bug; os.system will not expand the *
#	os.system(f"mv seg_{runstring}.* old_runstring")

#generate the .tpr file
#note that the restraint reference file (-r) selection assumes that minimization requires a single segment, which ought to be the case
# more general approach would involve checking the integrator in the mdp file
if run_number == 1:
	gmx_grompp_command = f"{gmxpath} grompp -f {mdpfiles[0]} -p ../input/topol.top -n ../input/index.ndx -o seg_{runstring}.tpr -c ../input/step5_input.gro -r ../input/step5_input.gro"

#start from minimization's .trr as there is no minimization checkpoint to use for NVT
#this is probably irrelevant because there are neither velocities nor a thermostat state from minimization and gen_vel = true for the first nvt round
elif run_number == 2: 
	gmx_grompp_command = f"{gmxpath} grompp -f {mdpfiles[0]} -p ../input/topol.top -n ../input/index.ndx -o seg_{runstring}.tpr -c seg_{last_runstring}.gro -r seg_0001.gro -t seg_{last_runstring}.trr -maxwarn 1"

#normal dynamics, using checkpoint .cpt to generate .tpr
#https://manual.gromacs.org/current/onlinehelp/gmx-grompp.html says that 
# Actually preserving the ensemble (if possible) still requires passing the checkpoint file to gmx mdrun -cpi.
# but I assume that this would conflict with the .tpr, which is necessary due to the changing restraints.
# preserving the ensemble is also by definition impossible across the NVT--> NPT switch
# inspection of previous run output files indicates that the last seg_####.cpt file is written at the end of the run 
else:
	gmx_grompp_command = f"{gmxpath} grompp -f {mdpfiles[0]} -p ../input/topol.top -n ../input/index.ndx -o seg_{runstring}.tpr -c seg_{last_runstring}.gro -r seg_0001.gro -t seg_{last_runstring}.cpt -maxwarn 2"

os.system(f"export GMX_NO_QUOTES=True; {gmx_grompp_command}")

#-----------------------------------------------------------------------------------------------------
#run simulation with mdrun
#-----------------------------------------------------------------------------------------------------

#indices of lines with already-read error messages
l_inds = []

#run gmx mdrun until a run completes successfully, then exit
for run_ind in range(16):
	#note that the pme gpu setting swtich assumes that minimization requires a single segment, which ought to be the case
	if run_number == 1:
		gmx_mdrun_command = f"{gmxpath} mdrun -v -deffnm seg_{runstring} -ntomp 8 -ntmpi 1"
	else:
		gmx_mdrun_command = f"{gmxpath} mdrun -v -deffnm seg_{runstring} -ntomp 8 -ntmpi 1 -nb gpu -bonded gpu -pme gpu -update gpu"

	gmx_mdr_out = os.system(f"export GMX_NO_QUOTES=True; export CUDA_VISIBLE_DEVICES=$SGE_GPU; {gmx_mdrun_command}")
	
	#check if the simulation crashed	
	crashed = False
	x = 0

	for line in open("seg_%s.log" % runstring):
		for errorline in error_lines:
			if errorline in line.strip() and (x not in l_inds):
				#record the indices of lines with error messages to avoid 
				#repeatedly exiting on the same error if the subsequent gromacs run worked fine
				#this is an issue if the seg_logs/ log file does not copy
				l_inds.append(x)

				crashed = True
				break
		if crashed:
			break

		x+=1

	#if no crash has been detected in seg_logs, check that a .gro file is present. Failed runs in which an mdrun job froze may leave no warning in seg_logs.
	if not crashed:
		if not os.path.exists("seg_%s.gro" % runstring):
			print("no .gro file found")
			crashed = True      #TODO: why was this commented out? Maybe the kinds of crashes which cause this problem aren't fixable by this anyway??? 

	if crashed:
		time.sleep(10) #this may not be useful

		#move files generated by mdrun to a backup directory for future inspection of root causes of errors
		mdrun_outputs = [".edr", ".gro", ".trr", ".xtc", ".log"] #"_prev.cpt", ".cpt", 

		failed_run_backup_dir = "failed_seg_%s_attempt_%s" % (runstring, run_ind)
		os.system("mkdir " + failed_run_backup_dir)

		for cfile in mdrun_outputs:
			os.system("mv seg_%s%s %s" % (runstring, cfile, failed_run_backup_dir))

	#proceed if the run did not crash
	else:
		break
