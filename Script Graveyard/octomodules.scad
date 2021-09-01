

rf = 10;

//sqrt2 = round(rf * sqrt(2))/rf;
//sqrt3 = round(rf * sqrt(3))/rf;
//sqrt6 = round(rf * sqrt(6))/rf;


sqrt2 = sqrt(2);
sqrt3 = sqrt(3);
sqrt6 = sqrt(6);


sqrt22 = sqrt2/2;
sqrt24 = sqrt2/4;

sqrt33 = sqrt3/3;

sqrt63 = sqrt6/3;





I = [1, 1, 1];
X = [1, 0, 0];
Y = [0, 1, 0];
Z = [0, 0, 1];

XY = X + Y;
YZ = Y + Z;


R0 = 0 * Z;
R45 = 45 * Z;
R90 = 90 * Z;
R180 = 180 * Z;
R270 = 270 * Z;

T_A = [1/2,     0,      sqrt24];
T_B = [-1/2,    0,      sqrt24];
T_C = [0,       1/2,    -sqrt24];
T_D = [0,       -1/2,   -sqrt24];

T_W = [1/2,     0,      -sqrt24];
T_X = [-1/2,    0,      -sqrt24];
T_Y= [0,       1/2,    sqrt24];
T_Z = [0,       -1/2,   sqrt24];

eps = 0.000;



module raw_octo(){
    intersection(){
        tilt = acos(sqrt33) * Y;
        
        rotate(R0)   scale(100) translate([-1/2, -1, 0]) rotate(tilt) translate(-X/2) cube([2, 2, 1 * sqrt63]);
        rotate(R90)  scale(100) translate([-1/2, -1, 0]) rotate(tilt) translate(-X/2) cube([2, 2, 1 * sqrt63]);
        rotate(R180) scale(100) translate([-1/2, -1, 0]) rotate(tilt) translate(-X/2) cube([2, 2, 1 * sqrt63]);
        rotate(R270) scale(100) translate([-1/2, -1, 0]) rotate(tilt) translate(-X/2) cube([2, 2, 1 * sqrt63]);
    }
}


module octahedron(
        iteration = 0,
        size = 1,
        overlap = 0,
        slit = 0,
        trim_front = 0,
        trim_back = 0,
        trim_left = 0,
        trim_right = 0,
        trim_top = 0,
        trim_bottom = 0,
        kern_front_left = 0,
        kern_front_right = 0,
        kern_back_left = 0,
        kern_back_right = 0,
        is_pyramid = 0
) {


    intersection(){
        if (iteration == 0){
            scale(size/100) raw_octo();
        } else {
            yao(iteration, size, 4 * overlap, slit);
        }
        
//        rotate(R0)   scale(size) translate([-1/2, -1, 0]) rotate(tilt) translate(-X/2) cube([2, 2, 1 * sqrt63]);
//        rotate(R90)  scale(size) translate([-1/2, -1, 0]) rotate(tilt) translate(-X/2) cube([2, 2, 1 * sqrt63]);
//        rotate(R180) scale(size) translate([-1/2, -1, 0]) rotate(tilt) translate(-X/2) cube([2, 2, 1 * sqrt63]);
//        rotate(R270) scale(size) translate([-1/2, -1, 0]) rotate(tilt) translate(-X/2) cube([2, 2, 1 * sqrt63]);
        


        
        trim_front = trim_front > 0 ? trim_front : -1;
        trim_back = trim_back > 0 ? trim_back : -1;
        trim_left = trim_left > 0 ? trim_left : -1;
        trim_right = trim_right > 0 ? trim_right : -1;
        trim_top = trim_top > 0 ? trim_top : -1;
        trim_bottom = trim_bottom > 0 ? trim_bottom : -1;
        kern_front_left = kern_front_left > 0 ? kern_front_left : -2;
        kern_front_right = kern_front_right > 0 ? kern_front_right : -2;
        kern_back_left = kern_back_left > 0 ? kern_back_left : -2;
        kern_back_right = kern_back_right > 0 ? kern_back_right : -2;

        // Kerning
        rotate(R45)
            translate([ - sqrt2 * (size/2 - kern_front_left), -sqrt2 * (size/2 - kern_front_right), -size])
            cube([sqrt2 * (size - kern_front_left -  kern_back_right), sqrt2 * (size - kern_front_right -  kern_back_left), 2 * size]);

         // Edge trimming
        translate([-size/2 + trim_left, -size/2 + trim_front, -sqrt22 * size + trim_bottom])
            cube([size - trim_left - trim_right, size - trim_front - trim_back, sqrt2 * size - trim_top - trim_bottom]);

        if (is_pyramid) translate(-size * XY) cube(size * [2, 2, 2]);
    }
}

module tetra(iteration = 0, size =1 , overlap = 0){
    if (iteration ==0){
        scale(sqrt22/2 * I * (size ))
        intersection(){
            translate(- Z-1.5 * X) rotate( acos(1/3)/2, X)  cube(3);
            translate(- Z-1.5 * X) rotate( - acos(1/3)/2 +90, X)  cube(3);
            translate( Z-1.5 * Y) rotate([acos(1/3)/2 + 180, 0, 90])  cube(3);
            translate( Z-1.5 * Y) rotate([-acos(1/3)/2 + 270, 0, 90])  cube(3);
        }
    } else {
        #octahedron(iteration-1, size/2, overlap);
        translate(size * [0, 1/4, sqrt22/4]) tetra(iteration -1, size/2, overlap);
        translate(size * [0, -1/4, sqrt22/4]) tetra(iteration -1, size/2, overlap);
        translate(size * [ 1/4,0, -sqrt22/4]) tetra(iteration -1, size/2, overlap);
        translate(size * [ -1/4,0, -sqrt22/4]) tetra(iteration -1, size/2, overlap);
    }
}



module yao(iteration, size, overlap, slit){
    module cuts(){
        translate((size- overlap/2) * T_A) octo_cuts(iteration, size - overlap/2, overlap, slit);
        slits(iteration, size - overlap/2, overlap, slit);
    }
    
    
    difference(){
        
        scale(size * I ) octahedron();
        rotate(R0) cuts();
        rotate(R90) cuts();
        rotate(R180) cuts();
        rotate(R270) cuts();
        mirror(Z) rotate(R0) cuts();
        mirror(Z) rotate(R90) cuts();
        mirror(Z) rotate(R180) cuts();
        mirror(Z) rotate(R270) cuts();
        
    }
    
}


module sub_octo(iteration, size, overlap, slit){
    
    
    translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, 1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, -1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, 0, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    
    mirror([0, 0, 1])translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([0, 0, 1])mirror([1, 1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([0, 0, 1])mirror([1, -1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([0, 0, 1])mirror([1, 0, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    
//    mirror([0, 0, 1]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
//    mirror([1, 1, 1]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
//    mirror([1, -1, 1]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
//    mirror([1, 0, 1]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
}


module sub_octo_sector(iteration, size, overlap, slit, weld_allowance = 0){
    difference(){
        intersection(){
            scale(size * I ) octahedron();
            rotate(-R45) translate(-weld_allowance * I) cube(size);
        }
        translate((size- overlap/2) * T_A) octo_cuts(iteration, size - overlap/2, overlap, slit);
        slits(iteration, size - overlap/2, overlap, slit);
    }
};

outer = 0;
face = 1;
edge = 2;

module octo_cuts(iteration, size, overlap, slit, position = outer){
    if (iteration > 0){
        if (position == outer){
            intersection() {
                cube((size - overlap - slit) * [1, 1, 2], center = true);
                scale(( (size * .999) - overlap ) * I ) tetra();
            }
            translate(size * T_B/2) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            translate(size * T_C/2) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            translate(size * T_D/2) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            translate(size * T_X/2) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            
            
            // For 3d printing the Koch surface
            
//            translate(size * T_B/2 + size/2) octo_cuts(1, size/2, overlap, slit, outer);
//            translate(size * T_C/2) octo_cuts(1, size/2, overlap, slit, outer);
//            translate(size * T_D/2) octo_cuts(1, size/2, overlap, slit, outer);
        }
        
        if (position == face) {
            intersection() {
                cube((size - overlap - slit) * [1, 1, 2], center = true);
                scale(( (size * .999) - overlap ) * I ) mirror(Z) tetra();
            }
            
            translate(size * T_X/2) octo_cuts(iteration - 1, size/2, overlap, slit, face); // prune
            
            translate(size * T_B/2) mirror(Z) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            translate(size * T_C/2) rotate(-R90) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            translate(size * T_D/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            
            translate(size * T_W/2) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            translate(size * T_Z/2) rotate(240, T_A) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            translate(size * T_Y/2) rotate(120, T_A) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
        }
        
        if (position == edge){
            intersection() {
                cube((size - overlap - slit) * [1, 1, 2], center = true);
                scale(( (size * .999) - overlap ) * I ) mirror(Z) tetra();
            }
            
            translate(size * T_C/2) rotate(-R90) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            translate(size * T_D/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, face);
//            
            translate(size * T_Z/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            translate(size * T_Y/2) rotate(-R90) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            
            translate(size * T_X/2) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            translate(size * T_W/2) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
        }
    }
}


module slits(iteration, size, overlap, slit, skip = false){
    
    
    
    ts = size;
    
    if (iteration > 0){// && !skip){
        length = size- overlap - sqrt22 * slit ;
        translate([length/2 + overlap/2 + slit/2,0, 0]) cube([length, slit, (overlap + 2*slit) * sqrt22], center = true);
    }
    
    if (iteration > 0){
        translate([0, 0, ts * sqrt22/2]) slits(iteration -1, size/2, overlap, slit, skip = false); // top
        translate([ts/4, ts/4, 0]) slits(iteration -1, size/2, overlap, slit, skip); // bottom right
        translate([ts/4, -ts/4, 0]) slits(iteration -1, size/2, overlap, slit, skip); // bottom left
        translate([ts/4, -ts/4, 0]) rotate(R90) slits(iteration -1, size/2, overlap, slit, skip = false); // inside left
        translate([ts/4, ts/4, 0]) rotate(-R90) slits(iteration -1, size/2, overlap, slit, skip = true); // inside right
        translate([0, 0, ts * sqrt22/2]) mirror(Z) slits(iteration -1, size/2, overlap, slit, skip = false); // inside top
    }
}




iteration = 2;
size = 100;
overlap = 10;
slit = 1;


//sub_octo(iteration, size, overlap, slit);



tetra(iteration = 5, size =10, overlap = 0);



//tetra(2);




//octahedron(
//    iteration = 3,
//    overlap = .1,
//    size = 4, 
//    trim_front = 0.0, 
//    trim_left = 0.0,
//    trim_back = 0.0,
//    trim_right = 0.0,
//    kern_front_left = 0, 
//    kern_back_right = .0, 
//    kern_front_right = 0, 
//    kern_back_left = .0,
//
//    is_pyramid = true);
//
//
//
//
//translate(4 * [1/2, 0, sqrt22/2]) rotate(R90) tetra(iteration = 3, size =4, overlap = .1);
//translate(4 * [1/2, 0, sqrt22/2]) octahedron(iteration=2, overlap = .1, size = 2);












//octahedron(
//    iteration = 2,
//    overlap = .1,
//    size = 2, 
//    trim_front = 0.05, 
//    trim_left = 0.0,
//    trim_back = 0.0,
//    trim_right = 0.0,
//    kern_front_left = 0.1, 
//    kern_back_right = .0, 
//    kern_front_right = .1, 
//    kern_back_left = .0,
//
//    trim_bottom = 0 * sqrt22);

