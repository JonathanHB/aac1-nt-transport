delete all

load /home/jonathan/Documents/grabelab/aac1-nt-transport/metadynamics/run4/run_c/1/mtd_seg_01.part0041.gro
fetch 6gciA

align mtd_seg_01.part0041, 6gciA and poly

center 6gciA and poly

hide everything
show cart
dss

util.cbag 6gciA
util.cbac mtd_seg_01.part0041

#side view
set_view (\
     0.356587350,    0.528710842,    0.770259202,\
    -0.748349190,   -0.331924945,    0.574277401,\
     0.559300780,   -0.781203926,    0.277301133,\
     0.000068597,    0.000199199, -184.835708618,\
   -21.651826859,   30.469146729,   -7.130819321,\
   146.850311279,  222.822296143,  -20.000000000 )

#png m_state_side_view, ray=1

#m view
set_view (\
     0.154419497,   -0.760281205,    0.630964518,\
    -0.862281144,   -0.415461928,   -0.289583296,\
     0.482311547,   -0.499353766,   -0.719732344,\
     0.000068597,    0.000199199, -152.736282349,\
   -21.651826859,   30.469146729,   -7.130819321,\
   109.463562012,  196.010208130,  -20.000000000 )

show spheres, mtd_seg_01.part0041 and resi 32+134+137+234+231+29 and not elem H and not name C+N+O
#show spheres, mtd_seg_01.part0041 and resi 79+279+235 and not elem H and not name C+N+O
color palecyan, mtd_seg_01.part0041 and not resi 32+134+137+234+231+29 and elem C
show spheres, resn ATP and not elem H
util.cbam resn ATP
color orange, name PA+PB+PG

set orthoscopic=on

png m_state_m_view, ray=1

#c view
#set_view (\
#     0.196003541,    0.739005923,   -0.644548535,\
#    -0.817093492,    0.486494482,    0.309318990,\
#     0.542162716,    0.466029972,    0.699191749,\
#     0.000007048,    0.000064135, -131.384445190,\
#   -22.526542664,   29.405048370,   -7.488833427,\
#    88.109367371,  174.656021118,  -20.000000000 )

#set_view (\
#     0.198935106,    0.738931358,   -0.643735528,\
#    -0.824847937,    0.480949104,    0.297170877,\
#     0.529197097,    0.471867293,    0.705184579,\
#     0.000012377,    0.000091098, -108.387992859,\
#   -31.708936691,   33.241264343,    2.592441559,\
#    66.824470520,  149.932922363,  -20.000000000 )

#set_view (\
#     0.198935106,    0.738931358,   -0.643735528,\
#    -0.824847937,    0.480949104,    0.297170877,\
#     0.529197097,    0.471867293,    0.705184579,\
#     0.000000000,    0.000000000,  -64.198959351,\
#   -30.067989349,   34.273643494,    3.668494225,\
#    22.644746780,  105.753204346,  -20.000000000 )

#hide sticks

#center 6gciA and resi 97+201+295+205+104+302+101+299+208

#show sticks, 6gciA and resi 97+201+295+205+104+302+101+299+208 and not elem H and not name C+N+O
#show sticks, mtd_seg_01.part0041 and resi 88+191+287+195+95+294+92+291+198 and not elem H and not name C+N+O

#color palecyan, mtd_seg_01.part0041 and not resi 88+191+287+195+95+294+92+291+198
#color palegreen, 6gciA and not resi 97+201+295+205+104+302+101+299+208