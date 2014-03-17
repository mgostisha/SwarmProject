import sys
import mylib
import test_solar

""" This NEEDS a data file as an argument! """

xi = sys.argv[1]
yi = sys.argv[2]
zi = sys.argv[3]
vxi = sys.argv[4]
vyi = sys.argv[5]
vzi = sys.argv[6]
sigpos = sys.argv[7]
sigvel = sys.argv[8]
n_part = sys.argv[9]
output_option = sys.argv[10]
n_steps = sys.argv[11]
t_total = sys.argv[12]
potential = sys.argv[13]
disk = sys.argv[14]
bulge = sys.argv[15]
halo = sys.argv[16]

test_solar.orbitFromInit(xi, yi, zi, vxi, vyi, vzi, sigpos, sigvel, n_part, output_option, n_steps, t_total, potential, disk, bulge, halo)
