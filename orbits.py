import newSwarm as ns
import mylib
import numpy

def orbitFromFile(filename, n_steps, t_tot, potential_optn, disk_optn, bulge_optn, halo_optn):

	initials = mylib.text2array(filename)
	n_steps = int(n_steps)
	t_tot = float(t_tot)

	for i in range(len(initials)):
		tmp = ns.Particle(initials[i], potential_optn)
		tmp.get_timesteps(t_tot, n_steps)
		tmp.compute_orbit(disk_optn, bulge_optn, halo_optn)
		output_fn = 'particle_'+str(i)+'.txt'
		tmp.write_file(output_fn)