import numpy
import mylib
import myfuncs as mf
import scipy.integrate as inte
import matplotlib as plt
from pylab import *

def orbitFromFile(filename, output_optn, n_steps, t_tot, potential_optn, disk_optn, bulge_optn, halo_optn):

	params = mylib.text2array(filename)
	n_steps = int(n_steps)+1
	t_tot = float(t_tot)
	t = numpy.linspace(0,t_tot,n_steps)
	orbits = numpy.zeros((len(t), len(params[0])))

	if(potential_optn == 'pointsrc'):
		for i in range(len(params[:])):
			initial = params[i]
			final = inte.odeint(mf.PointSource, initial, t)
			orbits = numpy.dstack((orbits, final))

	elif(potential_optn == 'wolfire'):
		for i in range(len(params[:])):
			initial = params[i]
			final = inte.odeint(mf.WolfirePotential, initial, t, args=(disk_optn, bulge_optn, halo_optn))
			orbits = numpy.dstack((orbits,final))

	mylib.outputStyle(orbits, output_optn)

def orbitFromInit(x, y, z, vx, vy, vz, sigmap, sigmav, n_particles, output_optn, n_steps, t_tot, potential_optn, disk_optn, bulge_optn, halo_optn):

	x = float(x); y = float(y); z = float(z);
	vx = float(vx); vy = float(vy); vz = float(vz);
	sigmap = float(sigmap); sigmav = float(sigmav); n_particles = int(n_particles);
	n_steps = int(n_steps)+1
	t_tot = float(t_tot)

	params = mylib.createInitArr(x, y, z, vx, vy, vz, sigmap, sigmav, n_particles)
	t = numpy.linspace(0,t_tot,n_steps)
	orbits = numpy.zeros((len(t),len(params[0])))

	if(potential_optn == 'pointsrc'):
		for i in range(len(params[:])):
			initial = params[i]
			final = inte.odeint(mf.PointSource, initial, t)
			orbits = numpy.dstack((orbits, final))

	elif(potential_optn == 'wolfire'):
		for i in range(len(params[:])):
			initial = params[i]
			final = inte.odeint(mf.WolfirePotential, initial, t, args=(disk_optn, bulge_optn, halo_optn))
			orbits = numpy.dstack((orbits,final))

	mylib.outputStyle(orbits, output_optn)
