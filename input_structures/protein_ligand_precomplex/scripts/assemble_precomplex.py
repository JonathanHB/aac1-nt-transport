#Jonathan Borowsky
#Grabe lab
#12/9/25

#######################  OUTLINE  #######################

#1. align the protein with its center of mass at the origin and its symmetry axis along the x, y, or z axis (see code from grant figures)
#2. align the ATP (in its ideal RCSB conformer) with its center of mass along the axis coincident to the protein symmetry axis and its long axis (by PCA) aligned with the same (with phosphates towards the protein)
#3. move the ATP as close to the protein as it can be while leaving room for a layer of waters
#4. rotate the ATP around the symmetry axis in 2pi/8 radian (1/8th circle) increments and save each

#                  not in this script
#5. build a membrane and solvate each structure in membrane builder
#6. extend all simulations until all ATP bind
#7. metadynamics



#######################  IMPORTS  #######################

import numpy as np
from sklearn.decomposition import PCA
import os

# allow the script to execute pymol commands
from pymol import cmd
# Import PyMOL's stored module.  This will allow us with a
# way to pull out the PyMOL data and modify it in our script.
from pymol import stored


#######################  PRELIMINARY  #######################

cmd.delete("all")
cmd.reset()

#######################  PROTEIN_DATA  #######################

def protdata(protein, state, debug=False):

    if protein == "aac1":

        if state == "c":
            prot_input_path = "/home/jonathan/Documents/grabelab/aac1-nt-transport/input_structures/protein/zenodo_7269191/btAAC1_cdl_cstate_2c3e.pdb"
        elif state == "m":
            prot_input_path = "/home/jonathan/Documents/grabelab/aac1-nt-transport/input_structures/protein/zenodo_7269191/btAAC1_cdl_mstate_6gci_model.pdb"
        else:
            print(f"invalid state {state}")
            return None

        #reference residues for AAC1, indices for models from zenodo 
        # based on the most stable parts of helices in the C state
        bent_helix_m_ends = [37, 142, 239]
        bent_helix_c_ends = [8, 113, 210]
        straight_helix_m_ends = [73, 176, 273]
        straight_helix_c_ends = [90, 193, 290]
    
    elif protein == "ucp1":

        prot_input_path = ""

        #reference residues for UCP1, indices for 8hbvA
        bent_helix_m_ends = [42, 142, 241]
        bent_helix_c_ends = [12, 112, 211]
        straight_helix_m_ends = [77, 176, 270]
        straight_helix_c_ends = [94, 193, 287]

    else:
        print(f"invalid protein {protein}")
        return None

    if debug:
        #check that the same number of residues were included from each third of the protein
        print([i-j for i,j in zip(bent_helix_m_ends, bent_helix_c_ends)])
        print([i-j for i,j in zip(straight_helix_c_ends, straight_helix_m_ends)])
        print(f"show cart, resi {' or resi '.join([str(i)+'-'+str(j) for i, j in zip(bent_helix_c_ends, bent_helix_m_ends)])}")
        print(f"show cart, resi {' or resi '.join([str(i)+'-'+str(j) for i, j in zip(straight_helix_m_ends, straight_helix_c_ends)])}")

    # helix_cterm_ends = bent_helix_m_ends+straight_helix_c_ends
    # helix_nterm_ends = bent_helix_c_ends+straight_helix_m_ends

    return prot_input_path, bent_helix_c_ends, bent_helix_m_ends, straight_helix_c_ends, straight_helix_m_ends #helix_cterm_ends, helix_nterm_ends

ligand_input_path = "/home/jonathan/Documents/grabelab/aac1-nt-transport/input_structures/ligand/ATP/ATP.cif"

#######################  PART 1: PROTEIN CENTERING AND ALIGNMENT  #######################

#-----------------------------------------------------------------------------------------
#define and load protein

protein = "aac1"
state = "m"

prot_input_path, bent_helix_c_ends, bent_helix_m_ends, straight_helix_c_ends, straight_helix_m_ends = protdata(protein, state, True)

cmd.load(prot_input_path, protein)
cmd.reset()

#rename chains and residue numbers to be consistent between C and M states
cmd.alter(f"{protein} and poly", "chain='A'")
cmd.alter(f"{protein} and poly", "segi='A'")

if state == "c":
    cmd.alter(f"resn CDL and segi C", "chain='B'")
    cmd.alter(f"resn CDL and segi C", "resi=1")
    cmd.alter(f"resn CDL and segi C", "segi='B'")

    cmd.alter(f"resn CDL and segi E", "chain='C'")
    cmd.alter(f"resn CDL and segi E", "resi=1") #2
    cmd.alter(f"resn CDL and segi E", "segi='C'")

    cmd.alter(f"resn CDL and segi D", "chain='D'")
    cmd.alter(f"resn CDL and segi D", "resi=1") #3
    cmd.alter(f"resn CDL and segi D", "segi='D'")

elif state == "m":
    cmd.alter(f"resn CDL and segi E", "chain='B'")
    cmd.alter(f"resn CDL and segi E", "resi=1")
    cmd.alter(f"resn CDL and segi E", "segi='B'")

    cmd.alter(f"resn CDL and segi D", "chain='C'")
    cmd.alter(f"resn CDL and segi D", "resi=1") #2
    cmd.alter(f"resn CDL and segi D", "segi='C'")

    cmd.alter(f"resn CDL and segi F", "chain='D'")
    cmd.alter(f"resn CDL and segi F", "resi=1") #3
    cmd.alter(f"resn CDL and segi F", "segi='D'")


#-----------------------------------------------------------------------------------------
#select symmetrical residues on stable helices and center protein

#symmetrical residue indices
bent_helix_inds = [[k for k in range(i, j+1)] for i,j in zip(bent_helix_c_ends, bent_helix_m_ends)]
straight_helix_inds = [[k for k in range(i, j+1)] for i, j in zip(straight_helix_m_ends, straight_helix_c_ends)]

# all_reference_inds = []
# for i in bent_helix_inds+straight_helix_inds:
#     all_reference_inds += i

#center protein
symm_resi_query = f"resi {' or resi '.join([str(i)+'-'+str(j) for i, j in zip(bent_helix_c_ends, bent_helix_m_ends)])}" + " or "\
      f"resi {' or resi '.join([str(i)+'-'+str(j) for i, j in zip(straight_helix_m_ends, straight_helix_c_ends)])}"

print(f"using CA of residues: {symm_resi_query}")

com_coords = cmd.centerofmass(f"{protein} and name CA and ({symm_resi_query})")
cmd.translate([-com_coords[0], -com_coords[1], -com_coords[2]], protein, camera=0)
cmd.reset()

#-----------------------------------------------------------------------------------------
#calculate points and create pseudoatoms on symmetry axis

#it turns out that the principal components of the well-ordered highly symmetric part of AAC1 are nearly degenerate,
# so its symmetry axis does not lie along any of them
#to get around this we calculate points on the symmetry axis
# by averaging the coordinates of alpha carbons of pseudosymmetric trios of residues

def make_symmetry_axis_pseudoatoms(atoms1, atoms2, atoms3, ps_index):

    axis_coords_all = []

    for i,j,k in zip(atoms1, atoms2, atoms3):

        i_coords = cmd.get_coords(f"resi {i} and name CA", 1)[0]
        j_coords = cmd.get_coords(f"resi {j} and name CA", 1)[0]
        k_coords = cmd.get_coords(f"resi {k} and name CA", 1)[0]

        axis_coords = np.mean(np.stack([i_coords, j_coords, k_coords]), axis=0)
        axis_coords_all.append(axis_coords)

        cmd.pseudoatom(f"pseudo_{ps_index}", pos=list(axis_coords))
        cmd.color("cyan", f"pseudo_{ps_index}")

        ps_index += 1

    return ps_index, np.stack(axis_coords_all)


#increment pseudoatom indices across both sets of helices avoid overwriting pseudoatoms
ps_ind = 0

ps_ind, coords_bent = make_symmetry_axis_pseudoatoms(bent_helix_inds[0], bent_helix_inds[1], bent_helix_inds[2], ps_ind)
cmd.color("red", "pseudo_*")
ps_ind, coords_straight = make_symmetry_axis_pseudoatoms(straight_helix_inds[0], straight_helix_inds[1], straight_helix_inds[2], ps_ind)

#-----------------------------------------------------------------------------------------
#align protein symmetry axis with z axis

def align_pc_to_z(coords, rotation_selection, objname=""):
    #calculate the first principal component of the symmetry axis pseudoatoms, which is the vector along the protein's symmetry axis
    #then take the cross product of this and the z axis, which is the rotation vector required to align the two
    pca = PCA(n_components=3)
    pca.fit(coords)

    pca_z_cross = np.cross(pca.components_[0], [0,0,1])
    axis_z_angle = np.arcsin(np.linalg.norm(pca_z_cross))*360/(2*np.pi)
    print(f"rotating {objname} {axis_z_angle} degrees to align with z axis")

    cmd.rotate([pca_z_cross[0], pca_z_cross[1], pca_z_cross[2]], -axis_z_angle, rotation_selection, camera=0, origin=[0,0,0])

prot_symmetry_axis_coords = np.concatenate((coords_bent, coords_straight))

align_pc_to_z(prot_symmetry_axis_coords, f"{protein} or pseudo*", "protein helix residue CA")

#needed to check pseudoatom center of mass
#cmd.alter("pseudo*", "elem='C'")

#-----------------------------------------------------------------------------------------
#show z axis

for i in range(-6,6):
    cmd.pseudoatom(f"pseudo_{ps_ind}", pos=[0,0,5*i])
    cmd.color("black", f"pseudo_{ps_ind}")
    cmd.show("spheres", f"pseudo_{ps_ind}")
    cmd.set("sphere_scale", 0.2)

    ps_ind+=1


#######################  PART 2: ATP CENTERING AND ALIGNMENT  #######################

#-----------------------------------------------------------------------------------------
#load or fetch the RCSB ideal ATP structure (which is conveniently already aligned) and alter its chain and segment ID

cmd.load(ligand_input_path)
#cmd.fetch("ATP")
cmd.alter("ATP", "chain='E'")
cmd.alter("ATP", "segi='E'")
cmd.alter("ATP", "resi=1")

cmd.reset()

#-----------------------------------------------------------------------------------------
#move the ATP out a little relative to the protein center of mass

#center ATP
atp_com_coords = cmd.centerofmass(f"ATP and not elem H")
cmd.translate([-atp_com_coords[0], -atp_com_coords[1], -atp_com_coords[2]], "ATP", camera=0)
cmd.reset()

#align ATP long axis with protein z axis
atp_ha_coords = cmd.get_coords(f"ATP and not elem H", 1)

align_pc_to_z(atp_ha_coords, "ATP", "ATP")

if state == "c":
    cmd.translate([0, 0, 4], "ATP", camera=0)
if state == "m":
    cmd.translate([0, 0, -10], "ATP", camera=0)



#######################  PART 3: ATP ROTATION AND OUTPUT  #######################

#-----------------------------------------------------------------------------------------
#create protein-ligand object, and save copies with ATP at different angles

os.chdir("/home/jonathan/Documents/grabelab/aac1-nt-transport/input_structures/protein_ligand_precomplex")

for angle_step in range(0,8):
    cmd.rotate("z", 360/8, "ATP", camera=0, origin=[0,0,0])

    cmd.create(f"prot_atp_angle_{angle_step}", f"{protein} or ATP")

    fnbase = f"{protein}_{state}_ATP_angle_{angle_step}"
    cmd.save(f"scratch/{fnbase}_with_anisou.pdb", f"prot_atp_angle_{angle_step}")  #not all of these actually have ANISOU records
    
    os.system(f"grep -v ANISOU scratch/{fnbase}_with_anisou.pdb > {fnbase}.pdb")




































