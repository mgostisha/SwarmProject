import sys
import mylib
import orbits

# Get parameters from shell script
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
drag_optn = sys.argv[16]
vfield = sys.argv[17]
vzero = sys.argv[18]
vRsc = sys.argv[19]
denfield = sys.argv[20]
nhcen = sys.argv[21]
nhcen2 = sys.argv[22]
Rscpow = sys.argv[23]
alphapow = sys.argv[24]
nhdisk1 = sys.argv[25]
Rscdisk1 = sys.argv[26]
Zscdisk1 = sys.argv[27]
nhdisk2 = sys.argv[28]
Rscdisk2 = sys.argv[29]
Zscdisk2 = sys.argv[30]
nhdisk3 = sys.argv[31]
Rscdisk3 = sys.argv[32]
Zscdisk3 = sys.argv[33]
colden = sys.argv[34]
sigden = sys.argv[35]
tol = sys.argv[36]
ps_mass = sys.argv[37]

# Send parameters to calculation function
orbits.orbitFromInit(xi, yi, zi, vxi, vyi, vzi, sigpos, sigvel, n_part, n_steps, t_total, potential, disk, bulge, halo,
	drag_optn, vfield, vzero, vRsc, denfield, nhcen, nhcen2, Rscpow, alphapow, nhdisk1, Rscdisk1, Zscdisk1, nhdisk2,
	Rscdisk2, Zscdisk2, nhdisk3, Rscdisk3, Zscdisk3, colden, sigden, tol, ps_mass)
