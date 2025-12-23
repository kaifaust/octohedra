include <config.scad>

intersection(){ 
    translate(( slit)/2 * Y )cube(2 * size * I);
    translate( undersize/4 * (X + Y)) rotate(-R90)import(sector_name);
}

