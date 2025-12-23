include <config.scad>

intersection(){ 
    translate(-undersize * Y)cube(2 * size * I);
    translate(sqrt22 * (undersize/2) * Z) mirror(Z) import(sector_name);
}
