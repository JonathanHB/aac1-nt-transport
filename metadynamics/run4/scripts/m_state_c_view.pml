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

set_view (\
     0.198935106,    0.738931358,   -0.643735528,\
    -0.824847937,    0.480949104,    0.297170877,\
     0.529197097,    0.471867293,    0.705184579,\
     0.000000000,    0.000000000,  -64.198959351,\
   -30.067989349,   34.273643494,    3.668494225,\
    22.644746780,  105.753204346,  -20.000000000 )

hide sticks

center 6gciA and resi 97+201+295+205+104+302+101+299+208

show sticks, 6gciA and resi 97+201+295+205+104+302+101+299+208 and not elem H and not name C+N+O
show sticks, mtd_seg_01.part0041 and resi 88+191+287+195+95+294+92+291+198 and not elem H and not name C+N+O

color palecyan, mtd_seg_01.part0041 and not resi 88+191+287+195+95+294+92+291+198
color palegreen, 6gciA and not resi 97+201+295+205+104+302+101+299+208

set orthoscopic=on

png m_state_c_view, ray=1