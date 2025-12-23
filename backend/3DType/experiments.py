import string

import svgelements
from fontTools import ttLib
from fontTools.ttLib import ttFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable


from xml.dom import minidom

import fontforge
import subprocess
from pathlib import Path
import svgutils





# of_interest = set("TV")
#
# print(of_interest)
#
# print(dir(myfont))
# my_glyphs = dict()
# for glyph in myfont.glyphs():
#     # print(glyph.glyphname)
#     if glyph.glyphname in of_interest:
#         print("yep")
#         my_glyphs[glyph.glyphname] = glyph


# print(my_glyphs)
#
# print(my_glyphs["T"].export("T.svg"))
# T = myfont["T"]
# print(myfont["T"].width)
# print(dir(myfont["T"]))
# # print(my_glyphs["T"].vwidth)

def generate_svg(font, character, svg_dir="svg"):
    Path(svg_dir).resolve().mkdir(exist_ok=True)
    out_file_name = str(Path(svg_dir).joinpath(f"{character}_{font.fontname}.svg").resolve())
    myfont[character].export(out_file_name)
    return out_file_name


def get_bounding_box(svg_file_name):
    with open(svg_file_name) as svg:
        doc = minidom.parse(svg)
        viewbox_attribute = doc.getElementsByTagName("svg")[0].getAttribute("viewBox")
        return map(int, viewbox_attribute.split())



def generate_stl(font, character, target_height_mm=25.4, svg_dir="svg", stl_dir="stl", type_high = 23.3172, relief = 3.175):
    svg_file_name = generate_svg(font, character, svg_dir)
    x_min, y_min, width, height = get_bounding_box(svg_file_name)
    Path(stl_dir).resolve().mkdir(exist_ok=True)
    out_file_name = str(Path(stl_dir).joinpath(f"{character}_{font.fontname}.stl").resolve())
    # width = font[character].width # + font[character].left_side_bearing + font[character].right_side_bearing
    lsb = font[character].left_side_bearing
    lsb = lsb if lsb >0 else 2 * abs(lsb)
    rsb = font[character].right_side_bearing
    rsb = rsb if rsb >0 else 2 * abs(rsb)
    # width += lsb + rsb
    width = font[character].width + lsb + rsb
    print(character, font[character].width, font[character].left_side_bearing, font[character].right_side_bearing)
    # print(width)
    subprocess.call(["OpenSCAD", "-o", out_file_name,
                     "--enable=lazy-union",
                     "--export-format", "binstl",
                     "-D", f'file_name="{svg_file_name!s}"',
                     "-D", f'target_height={target_height_mm}',
                     "-D", f'type_high={type_high}',
                     "-D", f'relief={relief}',
                     "-D", f'x_min={x_min}',
                     "-D", f'y_min={y_min}',
                     "-D", f'width={width}',
                     "-D", f'height={height}',
                     "-D", f'lsb={lsb}',
                     "-D", f'rsb={rsb}',
                     "-q",
                     "type.scad"])

# TEST_FILE = "Lobster Bisque.ttf"
TEST_FILE = "AGPfatschwarz-Regular.otf"
myfont = fontforge.open(TEST_FILE)


for glyph in myfont.glyphs():
    print(glyph.glyphname)




of_interest = list(string.ascii_uppercase) + [
    "period",
    "ampersand",
    "exclam"
]

for letter in myfont:
    generate_stl(myfont,letter)

# generate_svg(myfont, "D")



generate_stl(myfont, "J")

exit()

mysvg = svgelements.SVG.parse(TEST_FILE)

xmin, ymin, xmax, ymax = str(mysvg.viewbox).split()

print(xmin)

myfont = ttLib.TTFont("Lobster Bisque.ttf", recalcBBoxes=True)

print(myfont["head"].unitsPerEm)

font = myfont
cmap = font['cmap']
t = cmap.getcmap(3, 1).cmap
s = font.getGlyphSet()
units_per_em = font['head'].unitsPerEm


def getTextWidth(text, pointSize):
    total = 0
    for c in text:
        if ord(c) in t and t[ord(c)] in s:
            total += s[t[ord(c)]].width
        else:
            total += s['.notdef'].width
    total = total * float(pointSize) / units_per_em;
    return total


text = 'F'

width = getTextWidth(text, 12)

print('Text: "%s"' % text)
print('Width in points: %f' % width)
print('Width in inches: %f' % (width / 72))
print('Width in cm: %f' % (width * 2.54 / 72))
print('Width in WP Units: %f' % (width * 1200 / 72))

exit()

p = myfont.getGlyphSet().get("P")

print(dir(myfont))
print(myfont.glyf)
# print(p.width())

x = p.width()


def generate_type(font, character, target_height_mm=25.4, svg_dir="svg", stl_dir="stl"):
    pass

# out_file_name

# subprocess.call(["OpenSCAD", "-o", os.path.expanduser("~/Desktop/render_bin.stl"),
#                  "--enable=lazy-union",
#                  "--export-format", "binstl",
#                  "render.scad"])
