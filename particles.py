import mylib
import myfuncs as mf
import numpy
import math
import scipy.integrate as inte
from random import gauss

class Particle(object):

	fn_head = 'x\ty\tz\tvx\tvy\tvz\n-\t-\t-\t--\t--\t--'

	def __init__(self, arr, potential):
		self.arr = arr
		self.potential = potential
		self.Nc = self.arr[-1]
		self.arr = numpy.delete(self.arr, -1)

	def check_params(self):

		""" This function checks the input parameters to make sure they're valid, exits the program if they aren't. """

		invalids = ''
		if (math.fabs(self.arr[0]) > 50.0): invalids += 'error: x cannot be greater than |50.0| kpc; '
		if (math.fabs(self.arr[1]) > 50.0): invalids += 'error: y cannot be greater than |50.0| kpc; '
		if (math.fabs(self.arr[2]) > 30.0): invalids += 'error: z cannot be greater than |30.0| kpc; '
		if (math.fabs(self.arr[3]) > 1000.0): invalids += 'error: vx cannot be greater than |1000.0| km/s; '
		if (math.fabs(self.arr[4]) > 1000.0): invalids += 'error: vx cannot be greater than |1000.0| km/s; '
		if (math.fabs(self.arr[5]) > 1000.0): invalids += 'error: vx cannot be greater than |1000.0| km/s; '

		if (invalids != ''):
			print invalids
			raise SystemExit, 0

	def get_timesteps(self, time, steps):

		""" This function generates an array of constant timesteps to be used for the simulation. """

		self.t = numpy.linspace(0,time,steps)

	def gauss_coords(self, sigpos, sigvel, sigden):

		""" This function produces a coordinate from a gaussian distribution given the initial parameters. """

		x = gauss(self.arr[0], sigpos)
		y = gauss(self.arr[1], sigpos)
		z = gauss(self.arr[2], sigpos)
		vx = gauss(self.arr[3], sigvel)
		vy = gauss(self.arr[4], sigvel)
		vz = gauss(self.arr[5], sigvel)
		N_c = gauss(self.Nc, sigden)
		self.arr = numpy.array([x, y, z, vx, vy, vz])
		self.Nc = N_c

	def convert_units(self):

		""" This function converts the space coordinates, velocities, and column density to pc, M_sun, and Myr """
		self.arr[0] *= 1000.
		self.arr[1] *= 1000.
		self.arr[2] *= 1000.
		self.arr[3] *= 1.023
		self.arr[4] *= 1.023
		self.arr[5] *= 1.023
		self.Nc = (10 ** self.Nc) * (3.09e+18)**2

	def compute_orbit(self, disk_optn, bulge_optn, halo_optn, drag_optn, dragparams, vfield, denfield):

		""" This function calculates the orbits of the particle. """

		if(self.potential=='pointsrc'):
			self.orbit = inte.odeint(mf.PointSource, self.arr, self.t, rtol=1e-3, atol=1e-3, args=(drag_optn, dragparams,
				vfield, denfield, self.Nc))

		if(self.potential=='wolfire'):
			self.orbit = inte.odeint(mf.WolfirePotential, self.arr, self.t, rtol=1e-4, atol=1e-4, args=(disk_optn, bulge_optn,
				halo_optn, drag_optn, dragparams, vfield, denfield, self.Nc))

	def write_file(self, filename):

		""" This function takes the 2D array produced by the orbit calculation and writes it to a text file. """

		fn_head = 'x\ty\tz\tvx\tvy\tvz\n-\t-\t-\t--\t--\t--'
		to_write = numpy.savetxt(filename, self.orbit, delimiter='\t', header=fn_head, fmt='%.3f')

