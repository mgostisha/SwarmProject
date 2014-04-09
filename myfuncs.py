""" Functions to use with scipy.integrate.odeint """

import numpy as np
import mylib

def PointSource(y, t):
	""" Point Source Potential """

	# Define Constants 
	G = 4*(np.pi**2)
	M = 1.

	# Compute/designate spatial shorthands
	r = np.sqrt(y[0]**2 + y[1]**2 + y[2]**2)
	vx = y[3]
	vy = y[4]
	vz = y[5]

	# Compute gravitational accelerations
	gx = -y[0]/r * G*M/r/r
	gy = -y[1]/r * G*M/r/r
	gz = -y[2]/r * G*M/r/r

	return  vx, vy, vz, gx, gy, gz

def PointSourceWithDrag(y, t):
	""" Point Source Potential with Drag """

	# Define Constants
	G = 0.00449
	M = 10**10
	C_D = 1.
	denratio = 1./32400.

	# Compute/designate spatial shorthands
	r = np.sqrt(y[0]**2 + y[1]**2 + y[2]**2)
	vx = y[3]/1.023; vy = y[4]/1.023; vz = y[5]/1.023;
	v = np.sqrt(vx**2 + vy**2 + vz**2)

	# Compute gravitational accelerations
	gx = 0.5*C_D*v*vx*denratio - y[0]/r * G*M/r/r
	gy = 0.5*C_D*v*vy*denratio - y[1]/r * G*M/r/r
	gz = 0.5*C_D*v*vz*denratio - y[2]/r * G*M/r/r

	return vx, vy, vz, gx, gy, gz

def WolfirePotential(y, t, disk, bulge, halo, drag_optn, dragparams, velfield, denfield, N_c):
	""" All constants are in kpc (Ci, ai, bi) and km s^-1 (v_circ) """
	""" Accelerations derived from Wolfire et. al. 1995, Appendix A """

	# Define Constants

	C1 = 8.887; C2 = 3.0; C3 = 0.325;
	a1 = 6.5; a2 = 0.70; a3 = 12.0;
	b1 = 0.26; v_circ = 225.0;

	# Compute/designate spatial shorthands

	r = np.sqrt(y[0]**2 + y[1]**2)
	z = y[2]
	vx = y[3]; vy = y[4]; vz = y[5];
	vr = np.sqrt(vx**2 + vy**2)

	# Compute gravitational acceleration components

	gr1 = -C1*(v_circ**2)*r / (((r**2) + (a1 + np.sqrt(z**2 + b1**2))**2)**(3./2.))
	gr2 = -C2*(v_circ**2)*r / ((a2 + np.sqrt(z**2 + r**2))**2) / np.sqrt(z**2 + r**2)
	gr3 = -2.0*C3*(v_circ**2)*r / (a3**2 + r**2 + z**2)

	gz1 = -C1*(v_circ**2)*z*(1 + a1/np.sqrt(z**2 + b1**2)) / (((r**2) + (a1 + np.sqrt(z**2 + b1**2))**2)**(3./2.))
	gz2 = -C2*(v_circ**2)*z / ((a2 + np.sqrt(z**2 + r**2))**2) / np.sqrt(z**2 + r**2)
	gz3 = -2.0*C3*(v_circ**2)*z / (a3**2 + r**2 + z**2)

	# Turn off potential components the user doesn't want

	if (disk == 'no'):
		gr1 = 0;
		gz1 = 0;

	if (bulge == 'no'):
		gr2 = 0;
		gz2 = 0;

	if (halo == 'no'):
		gr3 = 0;
		gz3 = 0;

	# Add the components to get the total accelerations

	gr = (gr1+gr2+gr3) * (1.023)**2
	gz = (gz1+gz2+gz3) * (1.023)**2

	# Compute Drag
	if (drag_optn == 'yes'):
		drag_comps = mylib.computeDrag(dragparams, velfield, denfield, r, vr, gr, z, vz, N_c)
		gr = drag_comps[0] + gr
		gz = drag_comps[1] + gz


	gx = gr * y[0]/r
	gy = gr * y[1]/r

	return vx, vy, vz, gx, gy, gz










	

