import particles as part
import mylib
import numpy
import shutil

def orbitFromFile(filename, n_steps, t_tot, potential_optn, disk_optn, bulge_optn, halo_optn, drag_optn, 
	vfield, vzero, vRsc, denfield, nHcen, nHcen2, Rscpow, alphapow, nHdisk1, Rscdisk1, Zscdisk1, nHdisk2,
	Rscdisk2, Zscdisk2, nHdisk3, Rscdisk3, Zscdisk3, tol, ps_mass):

	#Read in file for initial arrays
	initials = mylib.text2array(filename)

	# Convert web entry strings to their respective data types
	# and convert to units of pc, M_sun, and Myr.
	n_steps = int(n_steps)
	t_tot = float(t_tot) * 1000.
	vzero = float(vzero) * 1.023
	vRsc = float(vRsc) * 1000.
	nHcen = (10 ** float(nHcen)) * (3.09e+18)**3
	nHcen2 = (10 ** float(nHcen2)) * (3.09e+18)**3
	nHdisk1 = (10 ** float(nHdisk1)) * (3.09e+18)**3
	nHdisk2 = (10 ** float(nHdisk2)) * (3.09e+18)**3
	nHdisk3 = (10 ** float(nHdisk3)) * (3.09e+18)**3
	Rscpow = float(Rscpow) * 1000.
	alphapow = float(alphapow)
	Rscdisk1 = float(Rscdisk1) * 1000.
	Rscdisk2 = float(Rscdisk2) * 1000.
	Rscdisk3 = float(Rscdisk3) * 1000.
	Zscdisk1 = float(Zscdisk1) * 1000.
	Zscdisk2 = float(Zscdisk2) * 1000.
	Zscdisk3 = float(Zscdisk3) * 1000.
	tol = 10 ** float(tol)
	ps_mass = 10 ** float(ps_mass)

	for i in range(len(initials)):
		tmp = part.Particle(initials[i], potential_optn, tol)
		tmp.get_timesteps(t_tot, n_steps)
		tmp.convert_units()
		dragparams = mylib.dragParameters(vfield, denfield, vzero, vRsc, nHcen, nHcen2, Rscpow, 
			alphapow, nHdisk1, Rscdisk1, Zscdisk1, nHdisk2, Rscdisk2, Zscdisk2, nHdisk3, Rscdisk3, Zscdisk3)
		tmp.compute_orbit(disk_optn, bulge_optn, halo_optn, drag_optn, dragparams, vfield, denfield, ps_mass)
		output_fn = 'particle_'+str(i)+'.txt'
		tmp.write_file(output_fn)
		#if (i==0):
		#	tmp.bokeh_plot()
		#	source = './sample_orbit.html'
		#	destination = '/d/www/gostisha/services/'
		#	shutil.move(source, destination)

def orbitFromInit(x, y, z, vx, vy, vz, sigpos, sigvel, n_particles, n_steps, t_tot, 
	potential_optn, disk_optn, bulge_optn, halo_optn, drag_optn, vfield, vzero, vRsc,
	denfield, nHcen, nHcen2, Rscpow, alphapow, nHdisk1, Rscdisk1, Zscdisk1, nHdisk2,
	Rscdisk2, Zscdisk2, nHdisk3, Rscdisk3, Zscdisk3, colden, sigden, tol, ps_mass):

	# Initialize array and convert to corrent data types
	initials = numpy.array([float(x), float(y), float(z), float(vx), float(vy), float(vz), float(colden)])

	# Convert web entry strings to their respective data types
	# and convert to units of pc, M_sun, and Myr.
	# (Since the initial space coordinates and velocities are
	# converted after choosing from gaussian, the std. deviations,
	# initial coordinates and velocities stay in their original units.)
	sigpos = float(sigpos)
	sigvel = float(sigvel)
	sigden = float(sigden)
	n_steps = int(n_steps)
	n_particles = int(n_particles)
	t_tot = float(t_tot) * 1000.
	vzero = float(vzero) * 1.023
	vRsc = float(vRsc) * 1000.
	nHcen = (10 ** float(nHcen)) * (3.09e+18)**3
	nHcen2 = (10 ** float(nHcen2)) * (3.09e+18)**3
	nHdisk1 = (10 ** float(nHdisk1)) * (3.09e+18)**3
	nHdisk2 = (10 ** float(nHdisk2)) * (3.09e+18)**3
	nHdisk3 = (10 ** float(nHdisk3)) * (3.09e+18)**3
	Rscpow = float(Rscpow) * 1000.
	alphapow = float(alphapow)
	Rscdisk1 = float(Rscdisk1) * 1000.
	Rscdisk2 = float(Rscdisk2) * 1000.
	Rscdisk3 = float(Rscdisk3) * 1000.
	Zscdisk1 = float(Zscdisk1) * 1000.
	Zscdisk2 = float(Zscdisk2) * 1000.
	Zscdisk3 = float(Zscdisk3) * 1000.
	tol = 10 ** float(tol)
	ps_mass = 10 ** float(ps_mass)

	for i in range(n_particles):
		tmp = part.Particle(initials, potential_optn, tol)
		tmp.get_timesteps(t_tot, n_steps)
		tmp.gauss_coords(sigpos, sigvel, sigden)
		tmp.convert_units()
		dragparams = mylib.dragParameters(vfield, denfield, vzero, vRsc, nHcen, nHcen2, Rscpow, 
			alphapow, nHdisk1, Rscdisk1, Zscdisk1, nHdisk2, Rscdisk2, Zscdisk2, nHdisk3, Rscdisk3, Zscdisk3)
		tmp.compute_orbit(disk_optn, bulge_optn, halo_optn, drag_optn, dragparams, vfield, denfield, ps_mass)
		output_fn = 'particle_'+str(i)+'.txt'
		tmp.write_file(output_fn)
		#if (i==0):
		#	tmp.bokeh_plot()
		#	source = './sample_orbit.html'
		#	destination = '/d/www/gostisha/services/'
		#	shutil.move(source, destination)




