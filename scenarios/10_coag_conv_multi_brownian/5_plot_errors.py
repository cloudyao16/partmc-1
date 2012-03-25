#!/usr/bin/env python

import numpy
import sys, os
sys.path.append("../../tool")
import mpl_helper
import matplotlib
import config

colors = ['b', 'r', 'g']
shapes = ['x', '.', '+']

(figure, axes) = mpl_helper.make_fig(figure_width=6, right_margin=2)

handles = []
labels = []
saved_shapes = []
shape_handles = []
shape_labels = []
for (i_part, (n_part, n_part_name, n_part_tex)) in enumerate(config.n_part_list):
    line_x = []
    err_x = []
    line_y = []
    err_y = []
    for (i_ratio, (ratio_type, ratio)) in enumerate(config.ratio_list):
        weight_type = "flat_source"
        name = "%s_%s_%s" % (n_part_name, ratio_type, weight_type)
        dirname = os.path.join(config.run_dirname, name)
        print dirname

        stats_filename = os.path.join(dirname, "stats.txt")
        stats = numpy.loadtxt(stats_filename)

        num_1_err_mean = stats[0]
        num_1_err_ci = stats[1]
        num_2_err_mean = stats[2]
        num_2_err_ci = stats[3]
        mass_1_err_mean = stats[4]
        mass_1_err_ci = stats[5]
        mass_2_err_mean = stats[6]
        mass_2_err_ci = stats[7]

        line_x.append(num_1_err_mean)
        line_y.append(num_2_err_mean)

        err_x.append(num_1_err_ci)
        err_y.append(num_2_err_ci)

        plot_extra = False
        if ratio == "0.999":
            plot_extra = True
            shape = 'o'
            shape_labels.append("equal weight")
        if ratio == "0.5":
            plot_extra = True
            shape = 's'
            shape_labels.append("equal number")
        if plot_extra:
            plotline = axes.plot([num_1_err_mean], [num_2_err_mean],
                                 color=colors[i_part], marker=shape, markerfacecolor='w',
                                 markeredgecolor=colors[i_part], markersize=8, markeredgewidth=1,
                                 linestyle='None')
            if shape not in saved_shapes:
                saved_shapes.append(shape)
                shape_handles.append(matplotlib.lines.Line2D([], [],
                                                             color=colors[i_part], marker=shape, markerfacecolor='w',
                                                             markeredgecolor='k', markersize=8, markeredgewidth=1,
                                                             linestyle='None'))
                #shape_handles.append(plotline)

    #(plotline, caplines, barlinecols) = axes.errorbar(line_x, line_y, err_y, err_x,
    #                                                  fmt=(colors[i_part] + ".-"))
    plotline = axes.plot(line_x, line_y, colors[i_part] + ".-")
    handles.append(plotline)
    labels.append("%s" % n_part_tex)

axes.set_xscale('log')
axes.set_yscale('log')
axes.set_xlabel(r'mean number 1 error $E[\|n_1 - n_{1, \rm s}\|_2]$')
axes.set_ylabel(r'mean number 2 error $E[\|n_2 - n_{2, \rm s}\|_2]$')
figure.legend(handles, labels, loc='upper right', numpoints=3)
figure.legend(shape_handles, shape_labels, loc='lower right', numpoints=1)
axes.grid(True)

figure.savefig(os.path.join(config.fig_dirname, "multi_errors.pdf"))
