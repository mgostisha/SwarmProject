import sys
import mylib
import test_solar

""" This NEEDS a data file as an argument! """

filename = sys.argv[1]
output_option = sys.argv[2]
n_steps = sys.argv[3]
t_total = sys.argv[4]
potential = sys.argv[5]
disk = sys.argv[6]
bulge = sys.argv[7]
halo = sys.argv[8]

test_solar.orbitFromFile(filename, output_option, n_steps, t_total, potential, disk, bulge, halo)
