load /home/jonathan/Documents/grabelab/aac1-nt-transport/metadynamics/run4/run_c/1/frame_676_ish.gro

hide everything

util.cbac poly
show sticks, resn ATP # and not elem H
util.cbam resn ATP
color orange, name PA+PB+PG
show cart

set orthoscopic=on

#show spheres, resi 88+191+287+195+95+294+92+291+198 and not elem H and not name C+N+O
#util.cbay resi 88+191+287+195+95+294+92+291+198
#show spheres, resi 32+134+137+234+231+29 and not elem H and not name C+N+O
show sticks, resi 32+134+137+234+79+235+279+126+127+130+83+179+183+186 and not elem H and not name C+N+O
util.cbag resi 79+235+279+126+127+130+83+179+183+186
util.cbay resi 32+134+137+234

show sticks, resi 126 and elem H
show sticks, resi 79 and name C+N+O


#set cartoon_transparency=0.5, resi 1-30

hide cart, resi 1-30
show ribbon, resi 1-31
color black, resi 1-31

hide cart, resi 281-999
show ribbon, resi 280-297
color black, resi 280-297

show dashes, measure*
hide labels, measure*
color black, measure*
set label_size=30

#set_view (\
#     0.459610403,   -0.290926486,    0.839110732,\
#    -0.886994600,   -0.197728932,    0.417287797,\
#     0.044516198,   -0.936089575,   -0.348932505,\
#     0.000263000,    0.000189034,  -66.239212036,\
#    44.594791412,   48.650665283,   53.070236206,\
#   -24.651205063,  157.029083252,   20.000000000 )

set_view (\
     0.604749322,   -0.277645588,    0.746443391,\
    -0.796250165,   -0.192418352,    0.573535323,\
    -0.015611549,   -0.941214800,   -0.337444037,\
     0.000263000,    0.000189034,  -67.281875610,\
    44.594791412,   48.650665283,   53.070236206,\
   -23.608535767,  158.071807861,   20.000000000 )

set ray_interior_color=cyan

#set surface_quality=0

png occluded_atp_coord_v1.png, ray=1
