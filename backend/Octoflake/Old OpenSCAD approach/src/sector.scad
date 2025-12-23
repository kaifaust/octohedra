









include <config.scad>






sqrt22 = sqrt(2)/2;
shift = 0.11;


//I = [1, 1, 1];
//X = [1, 0, 0];
//Y = [0, 1, 0];
//Z = [0, 0, 1];
//XY = X + Y;
//
//R0 = 0 * Z;
//R45 = 45 * Z;
//R90 = 90 * Z;
//R180 = 180 * Z;
//R270 = 270 * Z;
//
//T_A = [1/2,     0,      sqrt22/2];
//T_B = [-1/2,    0,      sqrt22/2];
//T_C = [0,       1/2,    -sqrt22/2];
//T_D = [0,       -1/2,   -sqrt22/2];
//
//T_W = [1/2,     0,      -sqrt22/2];
//T_X = [-1/2,    0,      -sqrt22/2];
//T_Y= [0,       1/2,    sqrt22/2];
//T_Z = [0,       -1/2,   sqrt22/2];
//
//eps = 0.01;



module octahedron() {

    module c(){
        translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
    }
    
    intersection(){
        rotate(R0) c();
        rotate(R90) c();
        rotate(R180) c();
        rotate(R270) c();
        mirror(Z) rotate(R0) c();
        mirror(Z) rotate(R90) c();
        mirror(Z) rotate(R180) c();
        mirror(Z) rotate(R270) c();
        
    }
}

module tetra(){
    scale(sqrt22/2 * I)
    intersection(){
        translate(- Z-1.5 * X) rotate( acos(1/3)/2, X)  cube(3);
        translate(- Z-1.5 * X) rotate( - acos(1/3)/2 +90, X)  cube(3);
        translate( Z-1.5 * Y) rotate([acos(1/3)/2 + 180, 0, 90])  cube(3);
        translate( Z-1.5 * Y) rotate([-acos(1/3)/2 + 270, 0, 90])  cube(3);
    }
}

module sub_octo(iteration, size, overlap, slit){
    
    
    rotate(R0) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, 1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, -1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, 0, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
}


module sub_octo_sector(iteration, size, overlap, slit, weld_allowance = 0){
    difference(){
        intersection(){
            scale(size * I ) octahedron();
            #rotate(-R45) translate(weld_allowance * I) cube(size);
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




//ref_size = 200;
//ref_i = 7;
//ref_n = 2 ^ ref_i;


//iteration = 2;
//n= 2 ^ iteration;
//size = ref_size/ref_n * n;
//overlap = 2 * .3  + .01;
//slit =  .001;



//render() octo_cuts(i, size, overlap, slit);
//sub_octo(iteration, size, overlap, slit);




echo(iteration, size, overlap);

sub_octo_sector(iteration-1, oversize/2, overlap, slit);

//rotate(R0) sub_octo_sector(iteration, oversize, overlap, slit);
//rotate(R90) sub_octo_sector(iteration, oversize, overlap, slit);
//rotate(R180) sub_octo_sector(iteration, oversize, overlap, slit);
//rotate(R270)  sub_octo_sector(iteration, oversize, overlap, slit);

//module ss(){
//    sub_octo_sector(iteration, oversize/2, overlap, slit);
//}
//
//
//
//
//
//
//module bottom(){
//    intersection(){ #translate(( slit)/2 * Y )cube(2 * size * I); translate(undersize/4 * (X + Y))ss();}
//}
//
//module top(){
//    translate(sqrt22 *(undersize/2) * Z) ss();
//}
//
//module inside_top(){
//    intersection(){ #translate(-undersize * Y)cube(2 * size * I); translate(sqrt22 * (undersize/2) * Z) mirror(Z) ss();}
//    
//    
//}
//
//module inside(){
//    intersection(){ #translate(( slit)/2 * Y )cube(2 * size * I); translate( undersize/4 * (X + Y)) rotate(-R90) ss();}
//    
//    
//    
//}
//
//rotate(R0) bottom();
//rotate(R0) mirror(Y) bottom();
//rotate(R90) bottom();
//rotate(R90) mirror(Y) bottom();
//rotate(R180) bottom();
//rotate(R180) mirror(Y) bottom();
//rotate(R270) bottom();
//rotate(R270) mirror(Y) bottom();
//
//rotate(R0) top();
//rotate(R90) top();
//rotate(R180) top();
//rotate(R270) top();
//
//rotate(R0) inside_top();
//rotate(R90) inside_top();
//rotate(R180) inside_top();
//rotate(R270) inside_top();
//
//rotate(R0) inside();
//rotate(R0) mirror(Y) inside();
//rotate(R90) inside();
//rotate(R90) mirror(Y) inside();
//rotate(R180) inside();
//rotate(R180) mirror(Y) inside();
//rotate(R270) inside();
//rotate(R270) mirror(Y) inside();
