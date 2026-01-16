#AAC1
#reference residues for AAC1, indices for models from zenodo 
# based on the most stable parts of helices in the C state
# bent_helix_m_ends = [37, 142, 239]
# bent_helix_c_ends = [8, 113, 210]
# straight_helix_m_ends = [73, 176, 273]
# straight_helix_c_ends = [90, 193, 290]

bent_helix_m_ends = [33, 138, 235]
bent_helix_c_ends = [8, 113, 210]
straight_helix_m_ends = [77, 180, 277]
straight_helix_c_ends = [90, 193, 290]

#check that the same number of residues were included from each third of the protein
print([i-j for i,j in zip(bent_helix_m_ends, bent_helix_c_ends)])
print([i-j for i,j in zip(straight_helix_c_ends, straight_helix_m_ends)])
a = f"color red, resi {' or resi '.join([str(i)+'-'+str(j) for i, j in zip(bent_helix_c_ends, bent_helix_m_ends)])}"
b = f"color red, resi {' or resi '.join([str(i)+'-'+str(j) for i, j in zip(straight_helix_m_ends, straight_helix_c_ends)])}"

print(f"{a}; {b}")