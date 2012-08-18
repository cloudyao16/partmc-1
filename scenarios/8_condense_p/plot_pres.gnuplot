# run from inside gnuplot with:
# load "<filename>.gnuplot"
# or from the commandline with:
# gnuplot -persist <filename>.gnuplot

set xlabel "time / s"
set ylabel "pressure / K"

set key center right

set ytics nomirror

plot "ref_condense_0001_env.txt" using 1:4 axes x1y1 with lines title "ref pressure", \
     "out_00000004/condense_0001_env.txt" using 1:4 axes x1y1 with points title "pressure"
