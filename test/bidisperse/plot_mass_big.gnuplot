# run from inside gnuplot with:
# load "<filename>.gnuplot"
# or from the commandline with:
# gnuplot <filename>.gnuplot

set logscale y
set xlabel "time (s)"
set ylabel "mass concentration (kg/m^3)"

plot "out/bidisperse_ode_data.txt" using 1:3 with lines title "ODE benchmark"
replot "out/bidisperse_mc_data.txt" using 1:3 with points title "particle method"