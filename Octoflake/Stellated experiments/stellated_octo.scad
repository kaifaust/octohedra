




module tetra(){
    points = [[-1,-1,-1], [1,1,-1], [-1,1,1], [1,-1,1]];
polyhedron(points, [[0,2,1], [0,1,3], [1,2,3], [0,3,2]]);
}

module s_tetra(iteration, size, overlap){
    if (iteration == 0){
        echo(size);
        scale(size + overlap) tetra();
    } else {
        echo(size);
        #rotate(R0) translate(size/2 * [1,-1,1]) s_tetra(iteration-1, size/2, overlap);
        mirror(Z) rotate(R90) translate(size/2 * [1,-1,1])
            s_tetra(iteration-1, size/2, overlap);
        rotate(R180) translate(size/2 * [1,-1,1]) s_tetra(iteration-1, size/2, overlap);
        mirror(Z) rotate(R270) translate(size/2 * [1,-1,1]) 
            s_tetra(iteration-1, size/2, overlap);
    }
}

module stellated_octo(iteration=0, size=1, overlap=0){
    s_tetra(iteration, size, overlap);
    rotate([0, 0, 90]) s_tetra(iteration, size, overlap);
    
}

module octo(){
    intersection(){
        tetra();
        rotate(R90) tetra();
    }
}
    
    
//#stellated_octo();
I = [1, 1, 1];
Z = [0, 0, 1];
R0 = [0, 0, 0];
R90 = [0, 0, 90];
R180 = [0, 0, 180];
R270 = [0, 0, 270];

sqrt22 = sqrt(2)/2;

iteration = 3;
size =4 * 2 ^ iteration;
overlap = 1;
s = size + overlap;

//octo();
//translate([.5, .5, .5]) rotate(0, [1, 1, 0]) scale(.5) octo();
//translate([-.5, -.5, .5]) rotate(0, [1, 1, 0]) scale(.5) octo();
//translate([.75, .75, .75]) rotate(0, [1, 1, 0]) scale(.25) octo();
//translate([-.75, -.75, .75]) rotate(0, [1, 1, 0]) scale(.25) octo();
//
//translate([-.5, .5, -.5]) rotate(0, [1, 1, 0]) scale(.5) octo();
//translate([.5, -.5, -.5]) rotate(0, [1, 1, 0]) scale(.5) octo();
//translate([-.75, .75, -.75]) rotate(0, [1, 1, 0]) scale(.25) octo();
//translate([.75, -.75, -.75]) rotate(0, [1, 1, 0]) scale(.25) octo();


//rotate(90, [1, -.5, 0]) octo();

//render()
//union(){
////    octo();
//     rotate(60, [1, 1, 1]) scale([.5, .5 ,1.1]) #octo();
//}

//stellated_octo(iteration, size, overlap);


//rotate(R0) translate(size * I) scale(s) stellated_octo();
//rotate(R90) translate(size * I) scale(s) stellated_octo();
//rotate(R180) translate(size * I) scale(s) stellated_octo();
//rotate(R270) translate(size * I) scale(s) stellated_octo();
//rotate(R0) translate(-size * I) scale(s) stellated_octo();
//rotate(R90) translate(-size * I) scale(s) stellated_octo();
//rotate(R180) translate(-size * I) scale(s) stellated_octo();
//rotate(R270) translate(-size * I) scale(s) stellated_octo();

//rotate(R0) translate(size/2 * [1,-1,1]) scale(s) tetra();
//mirror(Z) rotate(R90) translate(size/2 * [1,-1,1]) scale(s) tetra();
//rotate(R180) translate(size/2 * [1,-1,1]) scale(s) tetra();
//mirror(Z) rotate(R270) translate(size/2 * [1,-1,1]) scale(s) tetra();

//s_tetra(iteration, size, overlap);


render()
scale(50)
difference(){
    stellated_octo();
    intersection(){
//        tetra();
        rotate([0, 0, 0]) scale(1) stellated_octo(iteration = 4);
    }
}




