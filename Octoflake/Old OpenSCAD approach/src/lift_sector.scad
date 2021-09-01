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




//sector();



sector_name = "sector.stl";


            translate(undersize/4 * [1, 1, 0]) rotate(R0) trim_left() sector();
            translate(undersize/4 * [1, 1, 0]) rotate(R270) trim_front()sector();
mirror(Y)   translate(undersize/4 * [1, 1, 0]) rotate(R0) trim_left() sector();
mirror(Y)   translate(undersize/4 * [1, 1, 0]) rotate(R270) trim_front() sector();

            translate(undersize/4 * [0, 0, 2 * sqrt22]) rotate(R0) sector();
            translate(undersize/4 * [0, 0, 2 * sqrt22]) rotate(R0) mirror(Z) trim_top() sector();