




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




product = "none";

FRONT = "front";
TRIM_LEFT_KERN_RIGHT = "



if (product ==



front
trim left kern right
trim right
trim left
kern left
trim top































            










            

























            
mirror(Y)   translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R0) sector();
mirror(Y)   translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R0) mirror(Z) trim_top() sector();
mirror(Y)   translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R270) sector();
mirror(Y)   translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R270) mirror(Z) trim_top() sector();            
            
            
            
            translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R0) sector();
            translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R0) mirror(Z) trim_top() sector();
            translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R270) sector();
            translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R270) mirror(Z) trim_top() sector();
            
mirror(Y)   translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R0) sector();
mirror(Y)   translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R0) mirror(Z) trim_top() sector();
mirror(Y)   translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R270) sector();
mirror(Y)   translate(undersize/4 * [2, 2, 2 * sqrt22]) rotate(R270) mirror(Z) trim_top() sector();


            translate(undersize/4 * [4, 4, 2 * sqrt22]) rotate(R0) sector();
            translate(undersize/4 * [4, 4, 2 * sqrt22]) rotate(R0) mirror(Z) trim_top() sector();
            translate(undersize/4 * [4, 4, 2 * sqrt22]) rotate(R270) sector();
            translate(undersize/4 * [4, 4, 2 * sqrt22]) rotate(R270) mirror(Z) trim_top() sector();
            
mirror(Y)   translate(undersize/4 * [4, 4, 2 * sqrt22]) rotate(R0) sector();
mirror(Y)   translate(undersize/4 * [4, 4, 2 * sqrt22]) rotate(R0) mirror(Z) trim_top() sector();
mirror(Y)   translate(undersize/4 * [4, 4, 2 * sqrt22]) rotate(R270) sector();
mirror(Y)   translate(undersize/4 * [4, 4, 2 * sqrt22]) rotate(R270) mirror(Z) trim_top() sector();







            translate(undersize/4 * [1, 1, 4 * sqrt22]) rotate(R0) trim_left() sector();
            translate(undersize/4 * [1, 1, 4 * sqrt22]) rotate(R0) mirror(Z) trim_left()  sector();
            translate(undersize/4 * [1, 1, 4 * sqrt22]) rotate(R270) trim_front() sector();
            translate(undersize/4 * [1, 1, 4 * sqrt22]) rotate(R270) mirror(Z) trim_front()  sector();
mirror(Y)            translate(undersize/4 * [1, 1, 4 * sqrt22]) rotate(R0) trim_left() sector();
mirror(Y)            translate(undersize/4 * [1, 1, 4 * sqrt22]) rotate(R0) mirror(Z) trim_left()  sector();
mirror(Y)            translate(undersize/4 * [1, 1, 4 * sqrt22]) rotate(R270) trim_front() sector();
mirror(Y)            translate(undersize/4 * [1, 1, 4 * sqrt22]) rotate(R270) mirror(Z) trim_front()  sector();
            
            
            
            translate(undersize/4 * [0, 0, 6 * sqrt22]) rotate(R0) sector();
            translate(undersize/4 * [0, 0, 6 * sqrt22]) rotate(R0) mirror(Z) sector();
            
            
            translate(undersize/4 * [1, 1, 8 * sqrt22]) rotate(R0)  trim_left() sector();
            translate(undersize/4 * [1, 1, 8 * sqrt22]) rotate(R0) mirror(Z) trim_left() sector();
            translate(undersize/4 * [1, 1, 8 * sqrt22]) rotate(R270)  trim_front() sector();
            translate(undersize/4 * [1, 1, 8 * sqrt22]) rotate(R270) mirror(Z) trim_front() sector();            
            
            
mirror(Y)            translate(undersize/4 * [1, 1, 8 * sqrt22]) rotate(R0)  trim_left() sector();
mirror(Y)            translate(undersize/4 * [1, 1, 8 * sqrt22]) rotate(R0) mirror(Z) trim_left() sector();
mirror(Y)            translate(undersize/4 * [1, 1, 8 * sqrt22]) rotate(R270)  trim_front() sector();
mirror(Y)            translate(undersize/4 * [1, 1, 8 * sqrt22]) rotate(R270) mirror(Z) trim_front() sector();




            translate(undersize/4 * [0, 0, 10 * sqrt22]) rotate(R0) sector();
            translate(undersize/4 * [0, 0, 10 * sqrt22]) rotate(R0) mirror(Z) sector();