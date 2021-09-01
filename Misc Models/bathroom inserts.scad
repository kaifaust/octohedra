clearance = .25;

small_diameter = 37 - clearance;
big_diameter = 56 - clearance;

thickness = 1.27;

lip_width = 3;
lip_thickness = thickness;

height = 101;




module insert(diameter){
    difference(){
        union(){
            translate([0, 0, -height]) cylinder(height, d=diameter, $fn= 100);
            cylinder(lip_thickness, d=diameter + 2 * lip_width, $fn= 100);
        }
        
        translate([0, 0, -height + thickness + diameter/2])  cylinder(height + lip_thickness, d=diameter - 2 * thickness, $fn= 100);
        translate([0, 0, -height + thickness + diameter/2]) sphere(d=diameter - 2 * thickness, $fn = 100);
    };

}



//insert(small_diameter);

translate([0, 100, 0]) insert(big_diameter);