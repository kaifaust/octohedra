import subprocess





SCAD_PATH = "../OpenSCAD.app/Contents/MacOS/OpenSCAD"

SECTOR_FILE = "sector"
COMPOSE_FILE = "compose"




#subprocess.call(["ls", "-lha"])


cmd = [SCAD_PATH,]






iteration = 5;
overlap = 2 * .3  + .01;
slit =  .01;

ref_size = 200;
ref_i = 7;
ref_n = 2 ** ref_i;
n= 2 ** iteration;

size = ref_size/ref_n * n;





# iteration = 2;
# size = 25;
# overlap = 2;
# slit = .1;









def output_filename(filename, issimple = True):
    if (issimple):
        return f"{filename}.stl"
    return f"build/{filename}_{iteration}_{size}_{overlap}_{slit}.stl"


sector_name = output_filename("sector");
trim_top = output_filename("trim_top");
trim_bottom = output_filename("trim_bottom");
trim_insidetop = output_filename("trim_insidetop");
trim_insidebottom = output_filename("trim_insidebottom");



config = [
    "-D", f"{size=}",
    "-D", f"{iteration=}",
    "-D", f"{overlap=}",
    "-D", f"{slit=}",
     "-D", f'sector_name="{sector_name!s}"',
     "-D", f'trim_top="{trim_top!s}"',
     "-D", f'trim_bottom="{trim_bottom!s}"',
     "-D", f'trim_insidetop="{trim_insidetop!s}"',
     "-D", f'trim_insidebottom="{trim_insidebottom!s}"',
]


sector_cmd = [
    SCAD_PATH, 
    "-o", f"{SECTOR_FILE}_{iteration}.stl",
] + config + [f"{SECTOR_FILE}.scad"]




def run_scad(filename):
    cmd = [
        SCAD_PATH, 
        "-o", output_filename(filename),
        "--enable=lazy-union",
        "--export-format", "binstl",
        ] + config + [f"{filename}.scad"]

    print(cmd)
    subprocess.call(cmd)




run_scad("sector")
run_scad("trim_top")
run_scad("trim_insidetop")
run_scad("trim_insidebottom")
run_scad("trim_bottom")
# run_scad("compose")
run_scad("stellated")



#subprocess.run(sector_cmd)







