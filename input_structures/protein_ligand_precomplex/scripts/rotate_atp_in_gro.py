#from chatGPT

import numpy as np
import os
import MDAnalysis as mda
from MDAnalysis.analysis.pca import PCA
from MDAnalysis.transformations import rotate

# ---------------------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------------------

def spatial_pca(coords):
    """Compute eigenvectors/values of the 3×3 covariance of coordinates."""
    centered = coords - coords.mean(axis=0)
    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eigh(cov)

    # Sort eigenvalues/eigenvectors by decreasing variance
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    return eigvals, eigvecs


state = "c"
input_folder = os.getcwd() #"/home/jonathan/Documents/grabelab/aac1-nt-transport/charmmgui/membrane-builder-aac1-c-121025-2"
charmmgui_folder = [f for f in os.listdir(input_folder) if f.startswith("charmm-gui") and not f.endswith(".tgz")][0]
input_file = f"{input_folder}/{charmmgui_folder}/gromacs/step5_input.gro"

for increment in range(8):

    # Load the mixed system GRO file
    u = mda.Universe(input_file)

    # Select ATP molecule ONLY
    atp = u.select_atoms("resname ATP")

    # Store original positions so we can restore non-ATP atoms later
    original_positions = u.atoms.positions.copy()

    # --- Compute center of mass of the ATP molecule ---
    com = atp.center_of_mass()

    # ---- Compute spatial PCA (single-frame PCA) ----
    eigvals, eigvecs = spatial_pca(atp.positions)

    # First principal component (largest variance direction)
    pc1 = eigvecs[:, 0]
    pc1 = pc1 / np.linalg.norm(pc1)  # ensure normalization

    print("PC1 (ATP):", pc1)
    print("ATP COM:", com)

    # Rotation angle in radians
    angle_deg = 45.0*increment
    #angle_rad = np.deg2rad(angle_deg)

    # ---------------------------------------------------------
    # APPLY ROTATION ONLY TO ATP ATOMS
    # ---------------------------------------------------------

    # # 1. Center ATP at origin
    # atp.positions -= com

    # 2. Apply MDAnalysis built-in rotation around PC1 axis
    #the documentation of this contains a typo and is missing .rotateby
    atp_rotated = rotate.rotateby(angle=angle_deg, direction=pc1, point=com)(atp)
    atp.positions = atp_rotated.positions
    # # 3. Move ATP back to original location
    # atp.positions += com

    # ---------------------------------------------------------
    # RESTORE ALL NON-ATP ATOMS
    # ---------------------------------------------------------
    # Keep solvent, ions, other molecules exactly unchanged
    all_inds = u.atoms.indices
    non_atp = [item for item in all_inds if item not in atp.indices] #u.atoms.indices[~u.atoms.indices.isin(atp.indices)]
    u.atoms.positions[non_atp] = original_positions[non_atp]

    # ---------------------------------------------------------
    # WRITE OUT FINAL STRUCTURE
    # ---------------------------------------------------------

    with mda.Writer(f"{input_folder}/rotated-gro/aac1_{state}_ATP_angle_{increment}_post_charmmgui.gro", n_atoms=u.atoms.n_atoms) as W:
        W.write(u.atoms)

    #print("Done. Rotated ATP written to system_atp_rotated.gro")