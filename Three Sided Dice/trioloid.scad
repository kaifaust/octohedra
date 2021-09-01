diameter = 50;
radius = diameter / 2;



//module cap(){
//
//    intersection(){
//        sphere(d = diameter);
//
//
//        linear_extrude(diameter)
//        polygon([
//            radius * [cos(0), sin(0)],
//            radius * [cos(120), sin(120)],
//            radius * [cos(240), sin(240)]
//
//        ]);
//    }
//}
//
//
//
//
//
//hull(){
//    cap();
//
//
//    translate([0, 0, -radius])
//    rotate([0, 180, 0]) cap();
//}
twist = 0;
modifier = 10;

module coin(){
    rotate([0, -90 + twist, 0])
    intersection() {
        cylinder(h=0.1, d=diameter,center=true, $fn=100);
            translate([0, -radius, 0]) cube(diameter);
    }
}

module half_circle(){
    rotate([90, 0, 0])
    intersection() {
        cylinder(h=0.1, d=diameter,center=true);
        translate([0, -radius, 0]) cube(diameter);
    }
}


s = radius * sqrt(3)/3;
//d = cos(asin(1/3)) * diameter;



d =   radius;

echo(asin(1/3));
echo(cos(asin(1/3)));

t = radius * 0.25;

module cap(){
    rotate([0, 0, 0]) translate([s, 0, 0]) coin();
    rotate([0, 0, 120]) translate([s, 0, 0]) coin();
    rotate([0, 0, 240]) translate([s, 0, 0]) coin();
    
    rotate([0, 0, 60]) translate([0, 0, t]) half_circle();
    rotate([0, 0, 180]) translate([0, 0, t]) half_circle();
    rotate([0, 0, 300]) translate([0, 0, t]) half_circle();
}


cap();

translate( diameter * [2, 0, 0])
hull(){
    cap();
    translate([0,0,-d]) rotate([180, 0, 60]) cap();
}
//
//module coins(){
//    rotate([0, 0, 0]) translate([s, 0, 0]) coin();
//    rotate([0, 0, 120]) translate([s, 0, 0]) coin();
//    rotate([0, 0, 240]) translate([s, 0, 0]) coin();
//
//
//    rotate([0, 0, 60]) translate([s, 0, -d]) mirror([0,0,1])coin();
//    rotate([0, 0, 180]) translate([s, 0, -d]) mirror([0,0,1])coin();
//    rotate([0, 0, 300]) translate([s, 0, -d]) mirror([0,0,1])coin();
//}
//
//
//
//
//
//
//module o_coins(){
//    coin();
//    rotate([0, 0, 90]) translate([0, 0, -radius]) coin();
//}
//
//
//coins();
//translate([2 * diameter, 0, 0])
//hull(){ coins();}
//
//translate([0, 2 * diameter, 0]) o_coins();
//hull(){translate([2 * diameter, 2 * diameter, 0]) o_coins();};
//
//
//
//
//translate([4 * diameter, 0, 0])
//intersection(){
//    translate([-diameter, -diameter, -d/2]) cube(diameter * [2, 2, 2]);
//    hull(){ coins();}
//};
//
//
//
//module tri_coins(){
//    rotate([0, 0, 0]) translate([0, 0, 0]) half_circle();
//    rotate([0, 0, 120]) translate([0, 0, 0]) half_circle();
//    rotate([0, 0, 240]) translate([0, 0, 0]) half_circle();
//    
//    rotate([0, 0, 60]) translate([0, 0, -d]) half_circle();
//    rotate([0, 0, 180]) translate([0, 0, -d]) half_circle();
//    rotate([0, 0, 300]) translate([0, 0, -d]) half_circle();
//
//    
//}
//
//
//
//
//translate([0, -2 * diameter, 0]) tri_coins();
//
//hull(){
//    translate([2 * diameter, -2 *diameter, 0]) tri_coins();
//    
//    
//    
//}
//
//translate([4 * diameter, -2 * diameter, 0])
//intersection(){
//    translate([-diameter, -diameter, -d/2]) cube(diameter * [2, 2, 2]);
//    hull(){ tri_coins();}
//};