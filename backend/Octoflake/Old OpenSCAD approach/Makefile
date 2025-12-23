# Copyright 2015 Elena Grandi
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

BUILDDIR = build
CONFDIR = conf
SRCDIR = src

SLIC3R = slic3r

VPATH = $(SRCDIR):$(BUILDDIR)

STL_TARGETS = $(patsubst $(SRCDIR)/%.scad,$(BUILDDIR)/%.stl,$(wildcard $(SRCDIR)/*.scad))
GCODE_TARGETS = $(patsubst $(SRCDIR)/%.scad,$(BUILDDIR)/%.gcode,$(wildcard $(SRCDIR)/*.scad))

.PHONY: all gcode clean
all: $(STL_TARGETS)

gcode: $(GCODE_TARGETS)

$(BUILDDIR)/%.stl: %.scad $(SRCDIR)/lib/*
	mkdir -p ${BUILDDIR}
	openscad -o $@ $<

$(BUILDDIR)/%.gcode: %.stl ${CONFDIR}/basic.ini
	${SLIC3R} --load ${CONFDIR}/basic.ini $<

clean:
	rm -f ${BUILDDIR}/*.stl ${BUILDDIR}/*.gcode

