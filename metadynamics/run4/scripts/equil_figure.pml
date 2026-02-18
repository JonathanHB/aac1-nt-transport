#load /home/jonathan/Documents/grabelab/aac1-nt-transport/binding/rotated-cavity-atp/run01-aac1-c-atp-seg_06_centered.gro
hide everything
show cart
util.cbac
show sticks, byres(poly within 4 of resn ATP)
util.cbag byres(poly within 4 of resn ATP)
hide sticks, poly and elem H
hide sticks, poly and name C+N+O
show sticks, resn ATP and not elem H
util.cbam resn ATP
color orange, name PA+PB+PG
show sticks, resi 29 and not elem H and not name C+N+O
util.cbag resi 29

util.cbay resi 29+32+134+137+231+234

show dashes, measure*
show labels, measure*
color grey40, measure*
set label_size=30

set_view (\
     0.533948660,   -0.833708823,    0.140750766,\
    -0.844294429,   -0.516858697,    0.141429648,\
    -0.045165315,   -0.194355786,   -0.979882956,\
     0.000000000,   -0.000000000,  -57.115993500,\
    45.680000305,   48.290000916,   45.760002136,\
    37.256881714,   76.975105286,  -20.000000000 )