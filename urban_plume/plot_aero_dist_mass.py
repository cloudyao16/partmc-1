#!/usr/bin/env python
# Copyright (C) 2007 Matthew West
# Licensed under the GNU General Public License version 2 or (at your
# option) any later version. See the file COPYING for details.

import os, sys
import copy as module_copy
from Scientific.IO.NetCDF import *
from pyx import *
sys.path.append("../tool")
from pmc_data_nc import *
from pmc_pyx import *

times_hour = [0, 1, 6, 12, 24]
times_sec = [t * 3600 for t in times_hour]

data = pmc_var(NetCDFFile("out/testcase_withcoag/urban_plume_state_0001.nc"),
	       "aero", [])
data.write_summary(sys.stdout)
data.reduce([select("unit", "mass_den"),
             select("aero_species", "API1")])

data.scale(1)
data.scale_dim("radius", 1e6)

g = graph.graphxy(
    width = 10,
    x = graph.axis.log(min = 0.01,
		       max = 2,
		       title = "radius ($\mu$m)",
		       painter = grid_painter),
    y = graph.axis.log(
                       title = "mass density (kg/m$^3$)",
		       painter = grid_painter),
    key = graph.key.key(pos = "tr"))

for i in range(len(times_sec)):
    data_slice = module_copy.deepcopy(data)
    data_slice.reduce([select("time", times_sec[i])])
    g.plot(graph.data.list(data_slice.data_center_list(strip_zero = True),
			   x = 1, y = 2,
			   title = "%g hours" % times_hour[i]),
	   styles = [graph.style.line(lineattrs = [color_list[i]])])

g.writePDFfile("out/testcase_withcoag/aero_dist_API1.pdf")
