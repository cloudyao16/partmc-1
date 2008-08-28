#!/usr/bin/env python
# Copyright (C) 2007-2008 Matthew West
# Licensed under the GNU General Public License version 2 or (at your
# option) any later version. See the file COPYING for details.

import os, sys, math
import copy as module_copy
from Scientific.IO.NetCDF import *
from pyx import *
sys.path.append("../tool")
from pmc_data_nc import *
from pmc_pyx import *
import numpy

netcdf_dir = "out"
netcdf_re = re.compile(r"urban_plume_0.5_3am_state_0001_([0-9]{8})\.nc")
netcdf_re = re.compile(r"urban_plume_0.5_3am_state_0001_([0-9]{7}0)\.nc")
#netcdf_re = re.compile(r"urban_plume_0.5_3am_state_0001_(00000240)\.nc")

show_particles = [[1029, [0.02, 70], "wet diesel"],
                  [1892, [0.02, 45], "wet gasoline"],
                  [4116, [0.5, 70], "dry diesel"],
                  #[4167, [0.5, 40], "dry gasoline"],
                  [4186, [0.8, 45], "dry gasoline"],
                  ]

def process_file(in_filename, out_filename):
    ncf = NetCDFFile(in_filename)
    particles = read_particles(ncf)
    x_axis = pmc_log_axis(min = 1e-2, max = 2, n_bin = 160)
    y_axis = pmc_linear_axis(min = 0, max = 100, n_bin = 100)
    bin_array = numpy.zeros([x_axis.n_bin, y_axis.n_bin])
    show_coords = [[] for show in show_particles]
    particles.sort(cmp = lambda x,y: cmp(x.id, y.id))
    for particle in particles:
        diameter = particle.dry_diameter() * 1e6 # um
        comp_frac = particle.mass(include = ["BC"]) \
                    / particle.mass(exclude = ["H2O"]) * 100
        #water_frac = particle.mass(include = ["H2O"]) \
        #            / particle.mass() * 100
        #oc_frac = particle.mass(include = ["BC"]) \
        #            / particle.mass(include = ["BC", "OC"]) * 100
        #print "i=%6d d=%10e b=%10e w=%10e o=%10e" \
        #      % (particle.id, particle.dry_diameter() * 1e6,
        #         comp_frac, water_frac, oc_frac)
        x_bin = x_axis.find(diameter)
        y_bin = y_axis.find(comp_frac)
        bin_array[x_bin, y_bin] += 1.0 / particle.comp_vol \
                                   / x_axis.grid_size(x_bin) \
                                   / y_axis.grid_size(y_bin)
        for i, show in enumerate(show_particles):
            if particle.id == show[0]:
                show_coords[i] = [diameter, comp_frac]
    #max_val = bin_array.max()
    max_val = 1e10
    bin_array = bin_array / max_val
    for i in range(x_axis.n_bin):
        for j in range(y_axis.n_bin):
            bin_array[i,j] = min(1.0, bin_array[i,j])
            bin_array[i,j] = max(0.0, bin_array[i,j])

    g = graph.graphxy(
        width = 8,
        x = graph.axis.log(min = x_axis.min,
                           max = x_axis.max,
                           title = r'dry diameter ($\mu$m)'),
        y = graph.axis.linear(min = y_axis.min,
                              max = y_axis.max,
                              title = r"$f_{\rm BC,all}$",
                              texter = graph.axis.texter.decimal(suffix
                                                                 = r"\%")))

    start_time = 3 * 3600.0
    time_of_day = start_time + float(ncf.variables["time"].getValue())
    time_of_day = time_of_day % (24 * 3600.0)
    hours = int(time_of_day / 3600.0)
    minutes = int(time_of_day / 60.0) % 60
    seconds = int(time_of_day) % 60

    g.plot(graph.data.points(pmc_histogram_2d(bin_array, x_axis, y_axis),
                             xmin = 1, xmax = 2, ymin = 3, ymax = 4, color = 5),
           styles = [graph.style.rect(rainbow_palette)])
    boxed_text(g, 0.04, 0.9, "%02d:%02d LST" % (hours, minutes))
    for i in range(len(show_particles)):
        if len(show_coords[i]) > 0:
            label_point(g, show_coords[i][0], show_coords[i][1],
                        show_particles[i][1][0], show_particles[i][1][1],
                        show_particles[i][2])
    add_color_bar(g, min = 0.0, max = max_val,
                  title = r"number density", palette = rainbow_palette,
                  bar_x_offset = 0.8)
    g.writePDFfile(out_filename)
    ncf.close()


filenames = os.listdir(netcdf_dir)
for filename in filenames:
    match = netcdf_re.search(filename)
    if match:
        output_key = match.group(1)
        in_filename = os.path.join(netcdf_dir, filename)
        out_filename = os.path.join(netcdf_dir,
                                    "comp_2d_all_%s.pdf" % output_key)
        print in_filename
        process_file(in_filename, out_filename)