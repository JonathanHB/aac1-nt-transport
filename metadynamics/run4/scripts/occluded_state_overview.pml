load /home/jonathan/Documents/grabelab/aac1-nt-transport/metadynamics/run4/run_c/1/frame_676_ish.gro

hide everything

util.cbac poly
show spheres, resn ATP and not elem H
util.cbam resn ATP
color orange, name PA+PB+PG
show cart

create wat, resn TIP3+SOD+CLA
color grey70, wat
show surface, wat
set transparency=0.4, wat
set orthoscopic=on
set ray_interior_color=grey70

#show spheres, resi 88+191+287+195+95+294+92+291+198 and not elem H and not name C+N+O
#util.cbay resi 88+191+287+195+95+294+92+291+198
#show spheres, resi 32+134+137+234+231+29 and not elem H and not name C+N+O
#util.cbay resi 32+134+137+234+231+29


set_view (\
     0.427231193,   -0.008372325,    0.904095590,\
    -0.903923750,   -0.025628673,    0.426912934,\
     0.019595895,   -0.999632180,   -0.018517107,\
     0.000000000,    0.000000000, -186.938446045,\
    44.830566406,   46.062511444,   48.760093689,\
   163.211380005,  210.665496826,   20.000000000 )


#set_view (\
#     0.980747998,    0.064791977,    0.184187308,\
#    -0.184753954,    0.002830619,    0.982775629,\
#     0.063155122,   -0.997890890,    0.014746238,\
#     0.000000000,    0.000000000, -191.532333374,\
#    44.830566406,   46.062511444,   48.760093689,\
#   171.111953735,  211.952804565,   20.000000000 )

#set_view (\
#    -0.968212545,    0.065564848,   -0.241388574,\
#     0.241952837,    0.000694836,   -0.970287919,\
#    -0.063449547,   -0.997847319,   -0.016536454,\
#     0.000000000,    0.000000000, -167.950851440,\
#    44.830566406,   46.062511444,   48.760093689,\
#   146.685562134,  189.216110229,   20.000000000 )

set surface_quality=0

png occluded_overview_v2.png, ray=1
