iteration = 2;
size = 25;
overlap = 2;
slit = .1;

oversize = size + overlap/2;
undersize = size - overlap/2;
throat = overlap + slit;



sector_name = "sector.stl";
trim_top = "trim_top.stl";
trim_bottom = "trim_bottom.stl";
trim_insidetop = "trim_insidetop.stl";
trim_insidebottom = "trim_insidebottom.stl";



sqrt22 = sqrt(2)/2;


I = [1, 1, 1];
X = [1, 0, 0];
Y = [0, 1, 0];
Z = [0, 0, 1];

XY = X + Y;


R0 = 0 * Z;
R45 = 45 * Z;
R90 = 90 * Z;
R180 = 180 * Z;
R270 = 270 * Z;

T_A = [1/2,     0,      sqrt22/2];
T_B = [-1/2,    0,      sqrt22/2];
T_C = [0,       1/2,    -sqrt22/2];
T_D = [0,       -1/2,   -sqrt22/2];

T_W = [1/2,     0,      -sqrt22/2];
T_X = [-1/2,    0,      -sqrt22/2];
T_Y= [0,       1/2,    sqrt22/2];
T_Z = [0,       -1/2,   sqrt22/2];

eps = 0.01;