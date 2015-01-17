""" Functions to use with scipy.integrate.odeint """

import numpy as np
import mylib

def PointSource(y, t, drag_optn, dragparams, velfield, denfield, N_c, ps_mass):
	""" Point Source Potential """

	# Define Constants 
	G = 0.0045
	M = ps_mass

	# Compute/designate spatial shorthands
	z = y[2]
	r = np.sqrt(y[0]**2 + y[1]**2 + y[2]**2)
	vx = y[3]
	vy = y[4]
	vz = y[5]
	vr = np.sqrt(vx**2 + vy**2)

	# Compute gravitational accelerations
	gx = -y[0]/r * G*M/r/r
	gy = -y[1]/r * G*M/r/r
	gz = -y[2]/r * G*M/r/r

	gr = np.sqrt(gx**2 + gy**2)
	r2 = np.sqrt(y[0]**2 + y[1]**2)

	# Compute and add drag if wanted
	if (drag_optn == 'yes'):
		drag_comps = mylib.computeDrag(dragparams, velfield, denfield, r2, vr, gr, z, vz, N_c)
		gx = (vx/vr) * drag_comps[0] + gx
		gy = (vy/vr) * drag_comps[0] + gy
		gz = drag_comps[1] + gz

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
	# and convert from km/s to pc/Myr

	gr = (gr1+gr2+gr3) * (1.023)**2
	gz = (gz1+gz2+gz3) * (1.023)**2

	# Compute Drag
	if (drag_optn == 'yes'):
		drag_comps = mylib.computeDrag(dragparams, velfield, denfield, r, vr, gr, z, vz, N_c)
		dragx = (vx/vr) * drag_comps[0]
		dragy = (vy/vr) * drag_comps[0]
		dragz = drag_comps[1]

		gx = dragx + (y[0]/r) * gr
		gy = dragy + (y[1]/r) * gr
		gz = dragz + gz
	else:
		gx = (y[0]/r) * gr
		gy = (y[1]/r) * gr

	return vx, vy, vz, gx, gy, gz











	

