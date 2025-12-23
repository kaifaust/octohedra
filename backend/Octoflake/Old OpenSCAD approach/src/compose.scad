


include <config.scad>



//module ss(){
//    import(sub_flake_name);
////    sub_octo_sector(iteration - 1, size/2+ overlap/2, overlap, slit);
//}



//module bottom(){
//    intersection(){ #translate(( slit)/2 * Y )cube(2 * size * I); translate(undersize/4 * (X + Y))ss();}
//}
//
//module top(){
//    translate(sqrt22 *(undersize/2) * Z) ss();
//}
//
//module import(insidetop){
//    intersection(){ #translate(-undersize * Y)cube(2 * size * I); translate(sqrt22 * (undersize/2) * Z) mirror(Z) ss();}
//    
//    
//}
//
//module import(insidebottom){
//    intersection(){ #translate(( slit)/2 * Y )cube(2 * size * I); translate( undersize/4 * (X + Y)) rotate(-R90) ss();}
//    
//    
//    
//}





#translate(- throat/2 * [1, 1, 0]) cube(throat * [1, 1, 1]);

rotate(R0) import(trim_bottom);
rotate(R0) mirror(Y) import(trim_bottom);
rotate(R90) import(trim_bottom);
rotate(R90) mirror(Y) import(trim_bottom);
rotate(R180) import(trim_bottom);
rotate(R180) mirror(Y) import(trim_bottom);
rotate(R270) import(trim_bottom);
rotate(R270) mirror(Y) import(trim_bottom);

rotate(R0) import(trim_top);
rotate(R90) import(trim_top);
rotate(R180) import(trim_top);
rotate(R270) import(trim_top);

rotate(R0) import(trim_insidetop);
rotate(R90) import(trim_insidetop);
rotate(R180) import(trim_insidetop);
rotate(R270) import(trim_insidetop);

rotate(R0) import(trim_insidebottom);
rotate(R0) mirror(Y) import(trim_insidebottom);
rotate(R90) import(trim_insidebottom);
rotate(R90) mirror(Y) import(trim_insidebottom);
rotate(R180) import(trim_insidebottom);
rotate(R180) mirror(Y) import(trim_insidebottom);
rotate(R270) import(trim_insidebottom);
rotate(R270) mirror(Y) import(trim_insidebottom);




//rotate(R0) translate(undersize/4 * (X + Y))import(sub_flake_name);
//rotate(R0) mirror(Y) translate(undersize/4 * (X + Y))import(sub_flake_name);
//rotate(R90) translate(undersize/4 * (X + Y))import(sub_flake_name);
//rotate(R90) mirror(Y) translate(undersize/4 * (X + Y))import(sub_flake_name);
//rotate(R180) translate(undersize/4 * (X + Y))import(sub_flake_name);
//rotate(R180) mirror(Y) translate(undersize/4 * (X + Y))import(sub_flake_name);
//rotate(R270) translate(undersize/4 * (X + Y))import(sub_flake_name);
//rotate(R270) mirror(Y) translate(undersize/4 * (X + Y))import(sub_flake_name);

//rotate(R0) top();
//rotate(R90) top();
//rotate(R180) top();
//rotate(R270) top();
//
//rotate(R0) import(insidetop);
//rotate(R90) import(insidetop);
//rotate(R180) import(insidetop);
//rotate(R270) import(insidetop);
//
//rotate(R0) import(insidebottom);
//rotate(R0) mirror(Y) import(insidebottom);
//rotate(R90) import(insidebottom);
//rotate(R90) mirror(Y) inside();
//rotate(R180) inside();
//rotate(R180) mirror(Y) inside();
//rotate(R270) inside();
//rotate(R270) mirror(Y) inside();