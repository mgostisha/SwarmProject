import particles as part
import mylib
import numpy

def orbitFromFile(filename, n_steps, t_tot, potential_optn, disk_optn, bulge_optn, halo_optn):

	initials = mylib.text2array(filename)
	n_steps = int(n_steps)
	t_tot = float(t_tot)

	for i in range(len(initials)):
		tmp = part.Particle(initials[i], potential_optn)
		tmp.check_params()
		tmp.get_timesteps(t_tot, n_steps)
		tmp.compute_orbit(disk_optn, bulge_optn, halo_optn)
		output_fn = 'particle_'+str(i)+'.txt'
		tmp.write_file(output_fn)

def orbitFromInit(x, y, z, vx, vy, vz, sigpos, sigvel, n_particles, n_steps, t_tot, potential_optn, disk_optn, bulge_optn, halo_optn):

	initials = numpy.array([float(x), float(y), float(z), float(vx), float(vy), float(vz)])
	sigpos = float(sigpos); sigvel = float(sigvel);
	n_steps = int(n_steps); n_particles = int(n_particles)
	t_tot = float(t_tot)

	for i in range(n_particles):
		tmp = part.Particle(initials, potential_optn)
		tmp.check_params()
		tmp.get_timesteps(t_tot, n_steps)
		tmp.gauss_coords(sigpos, sigvel)
		tmp.compute_orbit(disk_optn, bulge_optn, halo_optn)
		output_fn = 'particle_'+str(i)+'.txt'
		tmp.write_file(output_fn)