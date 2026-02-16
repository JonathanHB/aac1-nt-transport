
import sys

fn_in = sys.argv[1]
fn_out = fn_in.split(".")[0]+"-helix-ca.pdb"

bent_helix_m_ends = [33, 138, 235]
bent_helix_c_ends = [8, 113, 210]
straight_helix_m_ends = [77, 180, 277]
straight_helix_c_ends = [90, 193, 290]

bent_helix_resis = [i for ct, nt in zip(bent_helix_m_ends, bent_helix_c_ends) for i in range(nt, ct+1)]
straight_helix_resis = [i for nt, ct in zip(straight_helix_m_ends, straight_helix_c_ends) for i in range(nt, ct+1)]
helix_resis = bent_helix_resis+straight_helix_resis
print("+".join([str(r) for r in helix_resis]))


with open(fn_out, "w") as f2:
    for line in open(fn_in):
        if line[0:4] == "ATOM" and line[13:15] == "CA" and int(line[23:26]) in helix_resis:
            f2.write(line)
        # elif line[0:4] == "ATOM" and line[17:20] == "ATP":
        #     f2.write(line)


