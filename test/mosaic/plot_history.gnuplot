# run from inside gnuplot with:
# load "<filename>.gnuplot"
# or from the commandline with:
# gnuplot -persist <filename>.gnuplot

set xlabel "time (s)"
set ylabel "gas mixing ratio (ppb)"
set y2label "aerosol mass concentration (kg/m^3)"

set key top left

set ytics nomirror
set y2tics

plot "out/mosaic_gas.txt" using 1:5 axes x1y1 with lines title "gas NH3"
replot "out/mosaic_gas.txt" using 1:7 axes x1y1 with lines title "gas NO2"
replot "out/mosaic_aero_species.txt" using 1:3 axes x1y2 with lines title "aerosol SO4"
replot "out/mosaic_aero_species.txt" using 1:4 axes x1y2 with lines title "aerosol NO3"
replot "out/mosaic_aero_species.txt" using 1:6 axes x1y2 with lines title "aerosol NH4"

replot "true_gas.txt" using 1:5 axes x1y1 with points title "true gas NH3"
replot "true_gas.txt" using 1:7 axes x1y1 with points title "true gas NO2"
replot "true_aero_species.txt" using 1:3 axes x1y2 with points title "true aerosol SO4"
replot "true_aero_species.txt" using 1:4 axes x1y2 with points title "true aerosol NO3"
replot "true_aero_species.txt" using 1:6 axes x1y2 with points title "true aerosol NH4"