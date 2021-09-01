













sqrt22 = sqrt(2)/2;
shift = 0.11;




module octahedron() {
    
//     octo_points = [
//        0.5 * [-1, -1, 0], // belt
//        0.5 * [ 1, -1, 0], 
//        0.5 * [ 1,  1, 0], 
//        0.5 * [-1,  1, 0], 
//        [0, 0, sqrt22], // top
//        [0, 0, -sqrt22], // bottom
//    ];
//
//    octo_faces = [
//        [0, 1, 4], // top pyramid
//        [1, 2, 4],
//        [2, 3, 4],
//        [3, 0, 4],
//        [1, 0, 5], // bottom pyramid
//        [2, 1, 5],
//        [3, 2, 5],
//        [0, 3, 5],
//    ];
//    
//
//
//    polyhedron(
//        points = octo_points,
//        faces = octo_faces
//    );
    
    
        intersection(){
        rotate(R0) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        rotate(R90) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        rotate(R180) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        rotate(R270) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        mirror(Z) rotate(R0) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        mirror(Z) rotate(R90) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        mirror(Z) rotate(R180) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        mirror(Z) rotate(R270) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        
    }
}

module octo_flake(size, iteration, overlap, slit, throat){
    intersection(){
        inner_flake(size - overlap, iteration, overlap, slit, throat); // Account for the overlap in the total size
        translate([-size, -size, 0]) cube([2, 2, 1] *  size); // Grab the top half
    }
}

 
 module inner_flake(size, iteration, overlap, slit, throat){
     assert(iteration >= 0, "Negative iteration value");
     assert(overlap > slit ||  overlap == 0 && slit == 0  , "Overlap must be greater than slit width");
     
     module smol(translation){
         translate(translation)
         inner_flake(size/2 + 0.01, iteration-1, overlap, slit, throat);
     }
     
     module smol_belt(shift, rotation){
         rotate([0, 0, rotation])
         intersection(){
             #translate([slit/2, slit/2, -size/2]) cube([size, size, size]);
             smol([shift, shift, 0]);
             
         }
     }
     
    if (iteration == 0) { 
        scale([1, 1, 1] * (size + overlap)) octahedron();
    } else {
        shift = 0.25 * size;

//        render()
        intersection() {
            scale((overlap + size) * [1, 1, 1]) octahedron();
            union() {
                cube(2*throat * [1, 1, 1], center=true);
                smol_belt(shift, 0);
                smol_belt(shift, 90);
                smol_belt(shift, 180);
                smol_belt(shift, 270);
                smol([0, 0, shift * 2 * sqrt22 - .001]); // Weld back together with top and bottom sub-octoflakes
                smol([0, 0, -shift * 2 * sqrt22 + .001]);
            };
        };
        
//        render()
//        union(){
//            difference(){
//                union () { 
//                    smol([shift, shift, 0]); // Assemble the belt of sub-octoflakes
//                    smol([shift, -shift, 0]) ;
//                    smol([-shift, -shift, 0]);
//                    smol([-shift, shift, 0]) ;
//                };
//          
//                cube([slit, 2 * size, size], center=true); // Chop apart the belt, to give continious cross-section
//                cube([2 * size, slit, size], center=true);
//          
//            };
//            cube(2*overlap * [1, 1, 1], center=true);
//            smol([0, 0, shift * 2 * sqrt22 - .001]); // Weld back together with top and bottom sub-octoflakes
//            smol([0, 0, -shift * 2 * sqrt22 + .001]);
//        };
      
    }  
 }
 
 
 



//octahedron();


//ref_size = 200;
//ref_i = 7;
//ref_n = 2 ^ ref_i;
//i = 3;
//n= 2 ^ i;
//size = ref_size/ref_n * n;
// 
//unit = 5;
//size = n * (unit-overlap) + overlap;
// 
//overlap = 1;
//slit = 0.5;
//throat = overlap + slit;
//
//
//echo(i, n, size);
//
//octo_flake(size, iteration = i , overlap = overlap, slit = slit, throat = throat);
 
 
 
  
 
 
 
 
 
 







I = [1, 1, 1];
X = [1, 0, 0];
Y = [0, 1, 0];
Z = [0, 0, 1];
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


module copy_mirror(vec=[0,1,0])
{
    children();
    mirror(vec) children();
}



module sub_octo(iteration, size, overlap = 0, slit = 0){
    
    
    
    rotate(R0) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, 1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, -1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
    mirror([1, 0, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit, slit/2);
//    rotate(R180) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit);
//    rotate(R270) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit);
    
    
    //// union of sectors 1:12 single sector 30
//    intersection() {
////        translate(size * [ -1, -1, 0]) cube( size * [2, 2, 1]);
//        union() {
//            rotate(R0) translate( size * X) sub_octo_sector(iteration, size, overlap, slit);
////            rotate(R90) translate( size * X) sub_octo_sector(iteration, size, overlap, slit);;
////            rotate(R180) translate( size * X) sub_octo_sector(iteration, size, overlap, slit);
////            rotate(R270) translate( size * X) sub_octo_sector(iteration, size, overlap, slit);
//        }
//    }
//    
    
    
    
//    module cuts() {
//        translate((size- overlap/2) * T_A) octo_cuts(iteration, size - overlap/2, overlap, slit);
//        slits(iteration, size - overlap/2, overlap, slit);
//    }
    
    
    
    
    //// Straight difference 1:25 -1 :23
//    difference() {
//        scale(size * I ) octahedron();
//        translate(-size * Z) cube( 2 * size * I, center = true);
//        
//
//        
//        rotate(R0) translate((size- overlap/2) * T_A) octo_cuts(iteration, size - overlap/2, overlap, slit);
//        rotate(R90) translate((size- overlap/2) * T_A) octo_cuts(iteration, size - overlap/2, overlap, slit);
//        rotate(R180) translate((size- overlap/2) * T_A) octo_cuts(iteration, size - overlap/2, overlap, slit);
//        rotate(R270) translate((size- overlap/2) * T_A) octo_cuts(iteration, size - overlap/2, overlap, slit);
//        
//                        rotate(R0) slits(iteration, size - overlap/2, overlap, slit);
//        rotate(R90) slits(iteration, size - overlap/2, overlap, slit);
//        rotate(R180) slits(iteration, size - overlap/2, overlap, slit);
//        rotate(R270) slits(iteration, size - overlap/2, overlap, slit);
//
//    }


        
    
    //// intersection of sectors 1:52
    
//    module sector() {
//    difference() {
//        scale(size * I ) octahedron();
//        translate(-size * Z) cube( 2 * size * I, center = true);
//        rotate(R0) translate((size- overlap/2) * T_A) octo_cuts(iteration, size - overlap/2, overlap, slit);
//        slits(iteration, size - overlap/2, overlap, slit);
//    }
//}
//    
//
//intersection(){
//            rotate(R0) sector();
//            rotate(R90) sector();
//            rotate(R180) sector();
//            rotate(R270) sector();
//}
    
    
    
}


module sub_octo_sector(iteration, size, overlap, slit, weld_allowance = 0){
    difference(){
        intersection(){
            scale(size * I ) octahedron();
            rotate(-R45) translate(weld_allowance * I) cube(size);
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
//        if (true){
//            intersection() {
//                cube((size - overlap - slit) * [1, 1, 2], center = true);
//                scale(( (size * .999) - overlap ) * I ) tetra();
//            }
//        }
        
        
        if (position == outer){
            intersection() {
                cube((size - overlap - slit) * [1, 1, 2], center = true);
                scale(( (size * .999) - overlap ) * I ) neo_tetra();
            }
            translate(size * T_B/2) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            translate(size * T_C/2) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            translate(size * T_D/2) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            translate(size * T_X/2) octo_cuts(iteration - 1, size/2, overlap, slit, face);


        }
        
        if (position == face) {
            intersection() {
                cube((size - overlap - slit) * [1, 1, 2], center = true);
                scale(( (size * .999) - overlap ) * I ) mirror(Z) neo_tetra();
            }
            
            translate(size * T_X/2) octo_cuts(iteration - 1, size/2, overlap, slit, face); // prune
            
            
            
            translate(size * T_B/2) mirror(Z) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            translate(size * T_C/2) rotate(-R90) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            translate(size * T_D/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            
            
            translate(size * T_W/2) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            translate(size * T_Z/2) rotate(240, T_A) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            translate(size * T_Y/2) rotate(120, T_A) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            
            
            
//            #translate(size * T_Z/2) translate(100 * T_A) rotate(120, T_A) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            
//            #translate(size * T_Z/2) rotate(240 * T_D) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
//            #translate(size * T_Z/2) rotate(240 * T_D) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
//            #translate(size * T_Z/2) rotate(240 * T_D) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
//            #translate(size * T_Z/2) rotate(240 * T_D) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
//            #translate(size * T_Z/2) rotate(240 * T_D) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
//            #translate(size * T_Z/2) rotate(240 * T_D) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
//            #translate(size * T_Z/2) rotate(240 * T_D) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            
            
//            translate(size * T_W/2) rotate(120 * T_A) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            
            
//            translate(size * T_X/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            translate(size * T_Y/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            translate(size * T_Z/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
            
            
            
            
        }
        
        if (position == edge){
            intersection() {
                cube((size - overlap - slit) * [1, 1, 2], center = true);
                scale(( (size * .999) - overlap ) * I ) mirror(Z) neo_tetra();
            }
            
            translate(size * T_C/2) rotate(-R90) octo_cuts(iteration - 1, size/2, overlap, slit, face);
            translate(size * T_D/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, face);
//            
            translate(size * T_Z/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            translate(size * T_Y/2) rotate(-R90) octo_cuts(iteration - 1, size/2, overlap, slit, outer);
            
            translate(size * T_X/2) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            translate(size * T_W/2) octo_cuts(iteration - 1, size/2, overlap, slit, edge);
            
            
            
        }

        
//        if (inner){
//            translate(size * T_A/2) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            translate(size * T_B/2) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            translate(size * T_C/2) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            translate(size * T_D/2) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//
//            
//            
//
////            translate(size * T_W/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            translate(size * T_X/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            translate(size * T_Y/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            translate(size * T_Z/2) rotate(R90) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//            
//            
//        } else {
//            translate(size * T_B/2) octo_cuts(iteration - 1, size/2, overlap, slit);
//            translate(size * T_C/2) octo_cuts(iteration - 1, size/2, overlap, slit);
//            translate(size * T_D/2) octo_cuts(iteration - 1, size/2, overlap, slit);
//            translate(size * T_X/2) mirror(Z) octo_cuts(iteration - 1, size/2, overlap, slit, inner = true);
//        }




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

//module tetra(){
//    tetra_points = [
//        [ -1, -1, -1],
//        [  1,  1, -1],
//        [ -1,  1,  1],
//        [  1, -1,  1],
//    ];
//
//    tetra_faces = [
//        [0, 1, 2],
//        [0, 3, 1],
//        [0, 2, 3],
//        [1, 3, 2]
//    ];
//
//    rotate(-45 * Z)
//    scale(sqrt22/2 * I)
//    polyhedron(
//        points = tetra_points,
//        faces = tetra_faces
//    );
//}

module neo_tetra(){
    scale(sqrt22/2 * I)
    intersection(){
        translate(- Z-1.5 * X) rotate( acos(1/3)/2, X)  cube(3);
        translate(- Z-1.5 * X) rotate( - acos(1/3)/2 +90, X)  cube(3);
        translate( Z-1.5 * Y) rotate([acos(1/3)/2 + 180, 0, 90])  cube(3);
        translate( Z-1.5 * Y) rotate([-acos(1/3)/2 + 270, 0, 90])  cube(3);
        
//                translate(- Z-1.5 * X) rotate( acos(1/3)/2, X)  cube(3);
//        translate(- Z-1.5 * X) rotate( - acos(1/3)/2 +90, X)  cube(3);
//        translate( Z-1.5 * Y) rotate([acos(1/3)/2 + 180, 0, 90])  cube(3);
//        translate( Z-1.5 * Y) rotate([-acos(1/3)/2 + 270, 0, 90])  cube(3);

        
        
        
    }
    
    
    
    
}


module neo_octahedron() {
    
    intersection(){
        rotate(R0) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        rotate(R90) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        rotate(R180) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        rotate(R270) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        mirror(Z) rotate(R0) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        mirror(Z) rotate(R90) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        mirror(Z) rotate(R180) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        mirror(Z) rotate(R270) translate([-1/2, -1, 0]) rotate(acos(sqrt(3)/3) * Y) translate(-1/2 * X) cube(2);
        
    }
}


//#octahedron();
//#neo_octahedron();


//ref_size = 200;
//ref_i = 7;
//ref_n = 2 ^ ref_i;
//
//i = 7;
//iteration = i;
//n= 2 ^ i;
//
//size = ref_size/ref_n * n;
//overlap = 2 * .3  + .01;
//slit =  .001;
//throat = overlap + slit;
//
//
//echo(i, n, size, overlap);


//iteration = 3;
//size = 100;
//overlap = 5;
//slit = 1;


//aug_tetra(size, overlap, slit);


//tetra();
//neo_tetra();

//render() octo_cuts(i, size, overlap, slit);
//sub_octo(i, size, overlap, slit);

module ss(){
    sub_octo_sector(iteration - 1, size/2+ overlap/2, overlap, slit);
}



XY = X + Y;
YX = X - Y;


module bottom(){
    intersection(){ #translate(( slit)/2 * Y )cube(2 * size * I); translate(size/4 * (X + Y))ss();}
}

module top(){
    translate(sqrt22 *(size/2) * Z) ss();
}

module inside_top(){
    intersection(){ #translate(-size * Y)cube(2 * size * I); translate(sqrt22 * (size/2) * Z) mirror(Z) ss();}
    
    
}

module inside(){
    intersection(){ #translate(( slit)/2 * Y )cube(2 * size * I); translate( size/4 * (X + Y)) rotate(-R90) ss();}
    
    
    
}

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


//translate(sqrt22 * size/2 * (X - Y)) ss();


//translate((size/2) * Z) ss();
//translate(sqrt22 * size/2 * (X + Y)) rotate(-R90) ss();
//translate(sqrt22 * size/2 * (X - Y)) rotate(R90) ss();
//translate(size/2 * Z) mirror(Z) ss();

//mirror([1, 1, 0]) translate(sqrt22 * size/2 * (X + Y)) ss();
//mirror([1, 1, 0]) translate(sqrt22 * size/2 * (X - Y)) ss();
//mirror([1, 1, 0]) translate((size/2) * Z) ss();
//mirror([1, 1, 0]) translate(sqrt22 * size/2 * (X + Y)) rotate(-R90) ss();
//mirror([1, 1, 0]) translate(sqrt22 * size/2 * (X - Y)) rotate(R90) ss();
//mirror([1, 1, 0]) translate(size/2 * Z) mirror(Z) ss();
//
//mirror([1, -1, 0]) translate(sqrt22 * size/2 * (X + Y)) ss();
//mirror([1, -1, 0]) translate(sqrt22 * size/2 * (X - Y)) ss();
//mirror([1, -1, 0]) translate((size/2) * Z) ss();
//mirror([1, -1, 0]) translate(sqrt22 * size/2 * (X + Y)) rotate(-R90) ss();
//mirror([1, -1, 0]) translate(sqrt22 * size/2 * (X - Y)) rotate(R90) ss();
//mirror([1, -1, 0]) translate(size/2 * Z) mirror(Z) ss();
//
//mirror([1, 0, 0]) translate(sqrt22 * size/2 * (X + Y)) ss();
//mirror([1, 0, 0]) translate(sqrt22 * size/2 * (X - Y)) ss();
//mirror([1, 0, 0]) translate((size/2) * Z) ss();
//mirror([1, 0, 0]) translate(sqrt22 * size/2 * (X + Y)) rotate(-R90) ss();
//mirror([1, 0, 0]) translate(sqrt22 * size/2 * (X - Y)) rotate(R90) ss();
//mirror([1, 0, 0]) translate(size/2 * Z) mirror(Z) ss();


//sub_octo_sector(iteration, size, overlap, slit);
//mirror([1, 1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit);


//translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit);
//mirror([1, 1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit);
//mirror([1, -1, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit);
//mirror([1, 0, 0]) translate( 0 * size * X) sub_octo_sector(iteration, size, overlap, slit);



//module sector() {
//    intersection(){
//        sub_octo(i, size, overlap, slit);
//        rotate(-R45) translate(-slit * I) cube(size);
//    }
//}


//render() {
//    intersection() {
//        translate(size * [ -1, -1, 0]) cube( size * [2, 2, 1]);
//        union() {
//            rotate(R0) sector();
 //           rotate(R90) sector();
 //           rotate(R180) sector();
 //           rotate(R270) sector();
 //       }
 //   }
//}

// // Testing whether we can do rotations easily
//intersection(){
//    rotate(R0) sub_octo(i, size, overlap, slit);
//    rotate(R90) sub_octo(i, size, overlap, slit);
//    rotate(R180) sub_octo(i, size, overlap, slit);
//    rotate(R270) sub_octo(i, size, overlap, slit);
//
//}


//slits(iteration, size-overlap/2, overlap, slit);


//render()

//difference() {
//    scale((size + overlap) * I ) octahedron();
//    translate(-size * I) cube(size * [2, 2, 1]);
//    sub_octo(iteration, size, overlap);
//}




//
//module sector(){
//    tetra_points = [
//        [ 0, 0, 0],
//        [ 1, 0, 0],
//        [ 0, 1, 0],
//        [ 0, 0, 1],
//    ];
//
//    tetra_faces = [
//        [0, 1, 2],
//        [0, 3, 1],
//        [0, 2, 3],
//        [1, 3, 2]
//    ];
//
//    rotate(-45 * Z)
////    scale(sqrt22/2 * I)
//    polyhedron(
//        points = tetra_points,
//        faces = tetra_faces
//    );
//}
//
//
//
//
//
//module sector_flake(iteration, size, overlap, slit){
//    intersection() {
//        translate(size * [ -1, -1, 0]) cube( size * [2, 2, 1]);
//        union() {
//            rotate(R0) sub_octo_sector(iteration, size, overlap, slit);;
//            rotate(R90) sub_octo_sector(iteration, size, overlap, slit);;
//            rotate(R180) sub_octo_sector(iteration, size, overlap, slit);
//            rotate(R270) sub_octo_sector(iteration, size, overlap, slit);
//        }
//    }
//}
//
//module sub_sector(iteration, size, overlap, slit){
//    
//    
//    module ss(jitter = 0){
//        sub_sector(iteration-1, size/2 + jitter, overlap, slit);
//    }   
//    
//
//
//    
//    if (iteration == 0){
//        scale((size + overlap) * I) sector();
//    } else {
//        translate(sqrt22 * size/2 * (X + Y)) ss(.001);
//        translate(sqrt22 * size/2 * (X - Y)) ss(.002);
//        translate((size/2) * Z) ss(.003);
//        
//        translate(sqrt22 * size/2 * (X + Y)) rotate(-R90) ss(.0015);
//        translate(sqrt22 * size/2 * (X - Y)) rotate(R90) ss(.0025);
//        translate(size/2 * Z) mirror(Z) ss(.0035);
//        
//        
//    }
//    
//    
//    
//    
//}
//
//
//
//ref_size = 200;
//ref_i = 8;
//ref_n = 2 ^ ref_i;
//i = 1;
//n= 2 ^ i;
//size = 100;
//overlap = 1;
//slit = .001;
//throat = overlap + slit;
//
//
//
////#sub_sector(0, size, overlap, slit);
//sub_sector(i, size, overlap, slit, jitter);



module stellated_octos(size = 100, iteration = 1){
    
    
    
    #scale(size) sub_octo(size, 3, );
    
//    rotate(R0) translate(size/2 * XY) scale(size/2) octahedron();
//    rotate(R90) translate(size/2 * XY) scale(size/2) octahedron();
//    rotate(R180) translate(size/2 * XY) scale(size/2) octahedron();
//    rotate(R270) translate(size/2 * XY) scale(size/2) octahedron();
    
    translate(sqrt22 * size * Z) scale(size/2) octahedron();
    
}




stellated_octos();









