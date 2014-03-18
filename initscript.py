import sys
import mylib
import orbits

xi = sys.argv[1]
yi = sys.argv[2]
zi = sys.argv[3]
vxi = sys.argv[4]
vyi = sys.argv[5]
vzi = sys.argv[6]
sigpos = sys.argv[7]
sigvel = sys.argv[8]
n_part = sys.argv[9]
n_steps = sys.argv[10]
t_total = sys.argv[11]
potential = sys.argv[12]
disk = sys.argv[13]
bulge = sys.argv[14]
halo = sys.argv[15]

orbits.orbitFromInit(xi, yi, zi, vxi, vyi, vzi, sigpos, sigvel, n_part, n_steps, t_total, potential, disk, bulge, halo)
