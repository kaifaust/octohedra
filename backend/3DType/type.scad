










file_name = "$H_LobsterBisque.svg";

target_height = 25.4;
type_high = .918 * 25.4;
relief = 1/8 * 25.4;
x_min = -10;
y_min = 0;
lsb = 0;
rsb = 0;
width = 1000;
height = 2048;
s = target_height/height;

echo(file_name, target_height, type_high, relief, width, height);





scale([s, s, 1])    translate([x_min + lsb, y_min, 0]) linear_extrude(type_high)  import(file_name, dpi=25.4);
scale([s, s, 1])    cube([width, height, type_high - relief]);


//type_high = 1000;
//relief = 100;
//inset = 2;
//
//x = -10;
//y = 0;
////svg_width = 1152; // G
////svg_width = 554; // I
//svg_width =1128; // H
//
//
//
//svg_height = 2048;
//
//target_height = 30;
//
//scale_factor = target_height / svg_height;
//scale_factor = 1;
//
//
//
//
//s = 480/2048;
//
//
//

//
//
//translate([2000, 0, 0])translate([10, 0, 0]) linear_extrude(type_high)  import("$G_LobsterBisque.svg");
//translate([2000, 0, 0]) scale([s, s, 1]) cube([1152, 2048, type_high-relief]);
//
//
//translate([4000, 0, 0])translate([10, 0, 0]) linear_extrude(type_high)  import("$H_LobsterBisque.svg");
//translate([4000, 0, 0]) scale([s, s, 1]) cube([1128, 2048, type_high-relief]);
//
//translate([6000, 0, 0])translate([10, 0, 0]) linear_extrude(type_high)  import("$I_LobsterBisque.svg");
//translate([6000, 0, 0]) scale([s, s, 1]) cube([554, 2048, type_high-relief]);

