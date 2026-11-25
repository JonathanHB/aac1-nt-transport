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

side view
set_view (\
     0.356587350,    0.528710842,    0.770259202,\
    -0.748349190,   -0.331924945,    0.574277401,\
     0.559300780,   -0.781203926,    0.277301133,\
     0.000068597,    0.000199199, -184.835708618,\
   -21.651826859,   30.469146729,   -7.130819321,\
   146.850311279,  222.822296143,  -20.000000000 )

png m_state_side_view, ray=1

#m view


#png m_state_m_view, ray=1



#hide sticks

#center 6gciA and resi 97+201+295+205+104+302+101+299+208

#show sticks, 6gciA and resi 97+201+295+205+104+302+101+299+208 and not elem H and not name C+N+O
#show sticks, mtd_seg_01.part0041 and resi 88+191+287+195+95+294+92+291+198 and not elem H and not name C+N+O

#color palecyan, mtd_seg_01.part0041 and not resi 88+191+287+195+95+294+92+291+198
#color palegreen, 6gciA and not resi 97+201+295+205+104+302+101+299+208

#set orthoscopic=on

#png m_state_c_view, ray=1