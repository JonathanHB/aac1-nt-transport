load /home/jonathan/Documents/grabelab/aac1-nt-transport/metadynamics/run4/run_c/1/frame_676_ish.gro

hide everything

util.cbac poly
show cart

set orthoscopic=on

show spheres, resi 88+191+287+195+95+294+92+291+198 and not elem H and not name C+N+O
util.cbay resi 195+95+294+92+291+198
util.cbac resi 88+191+287
#show spheres, resi 32+134+137+234+231+29 and not elem H and not name C+N+O
#util.cbay resi 32+134+137+234+231+29

set_view (\
    -0.755938590,   -0.650352955,   -0.074747734,\
    -0.653921366,    0.755502522,    0.039825901,\
     0.030571576,    0.078983486,   -0.996402204,\
     0.000581291,   -0.000381693, -130.697525024,\
    45.519046783,   45.397182465,   48.094497681,\
    97.502090454,  163.903457642,   20.000000000 )

set ray_interior_color=cyan

set surface_quality=0

png occluded_m_side_v1.png, ray=1
