include <config.scad>




module sector(){
    import(sector_name);
}

module trim_front(){
    intersection(){
        children();
        cube((undersize/2 - slit) * [1, 2, 2], center = true);
    }   
}

module trim_top(){
    intersection(){
        children();
        #cube(sqrt22 * undersize * [2, 2, 1], center = true);
    }   
}

module trim_left(){
    intersection(){
        children();
        translate(-(undersize - 2 * slit)/4 * Y) cube(2 * size * I); 
    }   
}

module trim_right(){
    intersection(){
        children();
        mirror(Y) translate(-(undersize - 2 * slit)/4 * Y) cube(2 * size * I); 
    }   
}

module kern_left(){
    intersection(){
        children();
        mirror(Y)translate((undersize - 2* slit)/4 * XY) rotate(225 * Z) translate(-size * Y) cube(2 * size, I);
    }
    
}

module kern_right(){
    intersection(){
        children();
         translate((undersize - 2* slit)/4 * XY) rotate(225 * Z) translate(-size * Y) cube(2 * size, I);
    }
    
}









//#translate(- throat/2 * [1, 1, 0]) cube(throat * [1, 1, 1]);





//module sector(){
//    import(sector_name);
//}



//trim_left() trim_front() sector();




module rot(){
    rotate(R0) children();
    rotate(R90) children();
    rotate(R180) children();
    rotate(R270) children();    
}
    


//translate(0 * size * 2/3 * Y) slitcorner_corner();
//translate(1 * size * 2/3 * Y) straight_corner();
//translate(2 * size * 2/3 * Y) straight_kern();
//translate(3 * size * 2/3 * Y) corner_kern();
//translate(4 * size * 2/3 * Y) straight_straight();

















module top(){
    translate(sqrt22 *(undersize/2) * Z) ss();
}

module insidetop(){
    intersection(){ #translate(-undersize * Y)cube(2 * size * I); translate(sqrt22 * (undersize/2) * Z) mirror(Z) ss();}
    
    
}







//ss();

// Bottom layer


echo(throat);

module welding_cube(){
    translate(-overlap/4 * XY) cube(overlap/2 * [1, 1, 1]);
}

include <stellated_sector.scad>
include <stellated_sector_90.scad>
include <stellated_sector_180.scad>
include <stellated_sector_270.scad>


