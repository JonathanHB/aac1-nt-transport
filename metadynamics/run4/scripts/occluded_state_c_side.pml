load /home/jonathan/Documents/grabelab/aac1-nt-transport/metadynamics/run4/run_c/1/frame_676_ish.gro

hide everything

util.cbac poly
show sticks, resn ATP and not elem H
util.cbam resn ATP
color orange, name PA+PB+PG
show cart

set orthoscopic=on

#show spheres, resi 88+191+287+195+95+294+92+291+198 and not elem H and not name C+N+O
#util.cbay resi 88+191+287+195+95+294+92+291+198
show spheres, resi 32+134+137+234+231+29 and not elem H and not name C+N+O
util.cbay resi 32+134+137+234+231+29

set_view (\
    -0.734645069,   -0.672956705,   -0.086121477,\
    -0.675502479,    0.737349927,    0.000527092,\
     0.063147798,    0.058562320,   -0.996281147,\
     0.000356286,   -0.000142183,  -81.424942017,\
    46.379474640,   46.363151550,   56.186000824,\
    69.058021545,   93.856529236,   20.000000000 )

set ray_interior_color=cyan

set surface_quality=0

png occluded_c_side_v1.png, ray=1
