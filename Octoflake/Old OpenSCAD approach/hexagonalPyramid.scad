


module octahedron() {
    
     octo_points = [
        [0, -1, 0], // belt
        [ 1, 0, 0], 
        [ 0,  1, 0], 
        [-1,  0, 0], 
        [0, 0, 1], // top
        [0, 0, -1], // bottom
    ];

    octo_faces = [
        [0, 1, 4], // top pyramid
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [1, 0, 5], // bottom pyramid
        [2, 1, 5],
        [3, 2, 5],
        [0, 3, 5],
    ];

    polyhedron(
        points = octo_points,
        faces = octo_faces
    );
}



module octoflake(i, size, center){
    
    if (i == 0){
        translate(center) scale(size) octahedron();
    } else {
        octoflake(i-1, size/2, center + 1/2 * size * [0, -1, 0]);
        octoflake(i-1, size/2, center + 1/2 * size * [1, 0, 0]);
        octoflake(i-1, size/2, center + 1/2 * size * [0, 1, 0]);
        octoflake(i-1, size/2, center + 1/2 * size * [-1, 0, 0]);
        octoflake(i-1, size/2, center + 1/2 * size * [0, 0, 1]);
        octoflake(i-1, size/2, center + 1/2 * size * [0, 0, -1]);
    }
    
    
}


//h = sqrt(2);
//h = sqrt(3)/2;
h = 1;
r = 1;


module hexBP(f = 6, h = 1, e = 1){
                      cylinder(h, r1=r, r2=0, $fn=f);
    mirror([0, 0, 1]) cylinder(h, r1=r, r2=0, $fn=f);   
}

//module tri(h = 1, e = 1){
//    
//                      cylinder(h, r1=sqrt(3)/2, r2=0, $fn=6);
//    mirror([0, 0, 1]) cylinder(h, r1=sqrt(3)/2, r2=0, $fn=6);  
//    
//}



//octoflake(2, 1, [0,0,0]);

module hex2(){
//    scale(   [2/sqrt(3), 2/sqrt(3), 1])
    rotate([0, 0, 0])
    union(){
    translate([0,0,-h]) hexBP(6);//cylinder(1, r1=1, r2=0, $fn=6);
    translate([0,0, h]) hexBP(6);

    rotate([0, 0, 000]) translate([1,0,0]) rotate([0, 0, 60]) hexBP(3);
    rotate([0, 0, 120]) translate([1,0,0]) rotate([0, 0, 60]) hexBP(3);
    rotate([0, 0, 240]) translate([1,0,0]) rotate([0, 0, 60]) hexBP(3);
    
    rotate([0, 0, 060]) translate([1,0,0])rotate([0, 0, 60]) hexBP(3);
    rotate([0, 0, 180]) translate([1,0,0])rotate([0, 0, 60]) hexBP(3);
    rotate([0, 0, 300]) translate([1,0,0])rotate([0, 0, 60]) hexBP(3);  
    }  
    
}

module tri2(){
    translate([0,0,-h]) hexBP(6);//cylinder(1, r1=1, r2=0, $fn=6);
    translate([0,0, h]) hexBP(6);

    rotate([0, 0, 000]) translate([1,0,0]) rotate([0, 0, 60]) hexBP(6);
    rotate([0, 0, 120]) translate([1,0,0]) rotate([0, 0, 60]) hexBP(6);
    rotate([0, 0, 240]) translate([1,0,0]) rotate([0, 0, 60]) hexBP(6);
    
//    rotate([0, 0, 060]) translate([1,0,0])rotate([0, 0, 60]) hexBP(3);
//    rotate([0, 0, 180]) translate([1,0,0])rotate([0, 0, 60]) hexBP(3);
//    rotate([0, 0, 300]) translate([1,0,0])rotate([0, 0, 60]) hexBP(3);    
    
}

//tri2();
translate([6, 0, 0]) tri2();


//translate([0,0,-2 * h]) hex2();
//translate([0,0, 2 * h]) hex2();
//
//rotate([0, 0,   0]) translate([2,0,0]) rotate([0, 0, 0]) hex2();
//rotate([0, 0, 120]) translate([2,0,0]) rotate([0, 0, 0])hex2();
//rotate([0, 0, 240]) translate([2,0,0]) rotate([0, 0, 0])hex2();

//rotate([0, 0, 30]) translate([sqrt(3),0,0]) rotate([0, 0, 30]) hex2();
//rotate([0, 0, 30 + 120]) translate([sqrt(3),0,0]) rotate([0, 0, 30]) hex2();
//rotate([0, 0, 30 + 240]) translate([sqrt(3),0,0]) rotate([0, 0, 30]) hex2();
//rotate([0, 0, 180]) translate([2,0,0]) hex2();
//rotate([0, 0, 300]) translate([2,0,0]) hex2(); 

module hex3(){
    rotate([0, 0, 00]) translate([0,0,-2 * h]) tri2();
    rotate([0, 0, 00]) translate([0,0, 2 * h]) tri2();
    //
    //rotate([0, 0,   0]) translate([2,0,0]) rotate([0, 0, 0]) hex2();
    //rotate([0, 0, 120]) translate([2,0,0]) rotate([0, 0, 0])hex2();
    //rotate([0, 0, 240]) translate([2,0,0]) rotate([0, 0, 0])hex2();

    rotate([0, 0, 0]) translate([2,0,0]) rotate([0, 0, 60]) tri2();
    rotate([0, 0, 0 + 120]) translate([2,0,0]) rotate([0, 0, 60]) tri2();
    rotate([0, 0, 0 + 240]) translate([2,0,0]) rotate([0, 0, 60]) tri2();
    //rotate([0, 0, 180]) translate([2,0,0]) hex2();
    //rotate([0, 0, 300]) translate([2,0,0]) hex2(); 
        
}

hex3();


//translate([0,0,-3* h]) hex3();
//translate([0,0, 3 * h]) hex3();
//rotate([0, 0, 0]) translate([3,0,0]) rotate([0, 0, 0]) hex3();
//rotate([0, 0, 0 + 120]) translate([3,0,0]) rotate([0, 0, 0]) hex3();
//rotate([0, 0, 0 + 240]) translate([3,0,0]) rotate([0, 0, 0]) hex3();


