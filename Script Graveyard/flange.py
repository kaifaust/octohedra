import drawSvg as draw
from math import cos, sin, radians


d = draw.Drawing(5.5, 5.5, origin='center', displayInline=False)

hole_diameter = 1/2 + 1/8
hole_radius = hole_diameter/2

# Draw a circle
d.append(draw.Circle(0, 0, 2.5,
                     fill='gray', stroke_width=.1, stroke='none'))

d.append(draw.Circle(0, 0, hole_radius,
                     fill='black', stroke_width=.1, stroke='black'))




d.append(draw.ArcLine(0,0, 1.25,0,60, stroke='black', fill="none", stroke_width=hole_diameter, stroke_linecap="round"))
# d.append(draw.ArcLine(0,0, 1.25 + hole_radius,0,60, stroke='black', fill="none", stroke_width=.1))



d.append(draw.ArcLine(0,0, 1.25,120,180, stroke='black', fill="none", stroke_width=hole_diameter, stroke_linecap="round"))
# d.append(draw.ArcLine(0,0, 1.25 + hole_radius,120,180, stroke='black', fill="none", stroke_width=.1))



d.append(draw.ArcLine(0,0, 1.25,240,300, stroke='black', fill="none", stroke_width=hole_diameter, stroke_linecap="round"))
# d.append(draw.ArcLine(0,0, 1.25 + hole_radius,240,300, stroke='black', fill="none", stroke_width=.1))




# d.append(draw.ArcLine(1.25, 0, hole_radius, 180, 0, stroke='black', fill="none", stroke_width=.1))
# d.append(draw.ArcLine(1.25 * cos(radians(60)), 1.25 * sin(radians(60)), hole_radius, 60, 270, stroke='black', fill="none", stroke_width=.1))
#
# d.append(draw.ArcLine(1.25 * cos(radians(120)), 1.25 * sin(radians(120)), hole_radius, -60, 120, stroke='black', fill="none", stroke_width=.1))
# d.append(draw.ArcLine(1.25 * cos(radians(180)), 1.25 * sin(radians(180)), hole_radius, 180, 0, stroke='black', fill="none", stroke_width=.1))
#
# d.append(draw.ArcLine(1.25 * cos(radians(240)), 1.25 * sin(radians(240)), hole_radius, 60, 240, stroke='black', fill="none", stroke_width=.1))
# d.append(draw.ArcLine(1.25 * cos(radians(300)), 1.25 * sin(radians(300)), hole_radius, -60, 120, stroke='black', fill="none", stroke_width=.1))

# # Draw an arbitrary path (a triangle in this case)
# p = draw.Path(stroke_width=2, stroke='lime',
#               fill='black', fill_opacity=0.2)
# p.M(-10, 20)  # Start path at point (-10, 20)
# p.C(30, -10, 30, 50, 70, 20)  # Draw a curve to (70, 20)
# d.append(p)

# Draw text
# d.append(draw.Text('Basic text', 8, -10, 35, fill='blue'))  # Text with font size 8
# d.append(draw.Text('Path text', 8, path=p, text_anchor='start', valign='middle'))
# d.append(draw.Text(['Multi-line', 'text'], 8, path=p, text_anchor='end'))
#
# # Draw multiple circular arcs
# d.append(draw.ArcLine(60,-20,20,60,270,
#                       stroke='red', stroke_width=5, fill='red', fill_opacity=0.2))
# d.append(draw.Arc(60,-20,20,60,270,cw=False,
#                   stroke='green', stroke_width=3, fill='none'))
# d.append(draw.Arc(60,-20,20,270,60,cw=True,
#                   stroke='blue', stroke_width=1, fill='black', fill_opacity=0.3))
#
# # Draw arrows
# arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=4, orient='auto')
# arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='red', close=True))
# p = draw.Path(stroke='red', stroke_width=2, fill='none',
#               marker_end=arrow)  # Add an arrow to the end of a path
# p.M(20, -40).L(20, -27).L(0, -20)  # Chain multiple path operations
# d.append(p)
# d.append(draw.Line(30, -20, 0, -10,
#                    stroke='red', stroke_width=2, fill='none',
#                    marker_end=arrow))  # Add an arrow to the end of a line

d.setPixelScale(1)  # Set number of pixels per geometry unit
d.setRenderSize(128,128)  # Alternative to setPixelScale
d.savePng('flamge.png')