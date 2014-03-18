import sys
import mylib
import orbits

""" This NEEDS a data file as an argument! """

filename = sys.argv[1]
n_steps = sys.argv[2]
t_total = sys.argv[3]
potential = sys.argv[4]
disk = sys.argv[5]
bulge = sys.argv[6]
halo = sys.argv[7]

orbits.orbitFromFile(filename, n_steps, t_total, potential, disk, bulge, halo)
