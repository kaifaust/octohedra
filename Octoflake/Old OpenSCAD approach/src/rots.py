
r90 = []
r180 = []
r270 = []


with open("stellated_sector.scad") as ss:



    for line in ss:
        if line.strip():
            r90.append("rotate(R90)" + line)
            r180.append("rotate(R180)" + line)
            r270.append("rotate(R270)" + line)



with open("stellated_sector_90.scad","w") as my_out:
    for line in r90:
        my_out.write(line)

with open("stellated_sector_180.scad","w") as my_out:
    for line in r180:
        my_out.write(line)

with open("stellated_sector_270.scad","w") as my_out:
    for line in r270:
        my_out.write(line)


