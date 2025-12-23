type_high = 0.914;
relief = 1/8;

union (){
scale(25.4 * [1, 1, 1]) translate([1/4, 1/16, 0]) linear_extrude(height = type_high) scale(1/100 * [1, 1, 1]) import("pool chop.svg");
//scale([4, 4, 1])scale(25.4) translate([1/4, 1/16, 0]) linear_extrude(height = type_high) scale(1/100 * [1, 1, 1]) import("pool chop.svg");

scale(25.4) cube([2, 2, type_high - relief]);
}

