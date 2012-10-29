
set terminal postscript eps color
set output "aero_size_mass.eps"

set logscale
set grid
set xlabel "wet diameter D / um"
set ylabel "mass conc m / (ug m^{-3})"

plot "ship_plume_wc_0001_aero_size_mass.txt" using ($1*1e6):($2*1e9) title "t = 0 s", \
     "ship_plume_wc_0001_aero_size_mass.txt" using ($1*1e6):($3*1e9) title "t = 10 s", \
     "ship_plume_wc_0001_aero_size_mass.txt" using ($1*1e6):($6*1e9) title "t = 40 s", \
     "ship_plume_wc_0001_aero_size_mass.txt" using ($1*1e6):($11*1e9) title "t = 100 s"