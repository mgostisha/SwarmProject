import sys
import mylib
import orbits

# This NEEDS a data file as an argument!
# Get parameters from shell script

filename = sys.argv[1]
n_steps = sys.argv[2]
t_total = sys.argv[3]
potential = sys.argv[4]
disk = sys.argv[5]
bulge = sys.argv[6]
halo = sys.argv[7]
drag_optn = sys.argv[8]
vfield = sys.argv[9]
vzero = sys.argv[10]
vRsc = sys.argv[11]
denfield = sys.argv[12]
nhcen = sys.argv[13]
nhcen2 = sys.argv[14]
Rscpow = sys.argv[15]
alphapow = sys.argv[16]
nhdisk1 = sys.argv[17]
Rscdisk1 = sys.argv[18]
Zscdisk1 = sys.argv[19]
nhdisk2 = sys.argv[20]
Rscdisk2 = sys.argv[21]
Zscdisk2 = sys.argv[22]
nhdisk3 = sys.argv[23]
Rscdisk3 = sys.argv[24]
Zscdisk3 = sys.argv[25]
tol = sys.argv[26]
ps_mass = sys.argv[27]

# Send parameters to calculation function
orbits.orbitFromFile(filename, n_steps, t_total, potential, disk, bulge, halo, drag_optn, vfield, vzero, vRsc,
	denfield, nhcen, nhcen2, Rscpow, alphapow, nhdisk1, Rscdisk1, Zscdisk1, nhdisk2, Rscdisk2, Zscdisk2, nhdisk3,
	Rscdisk3, Zscdisk3, tol, ps_mass)
