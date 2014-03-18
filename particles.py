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

	def check_params(self):
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
		self.t = numpy.linspace(0,time,steps)

	def gauss_coords(self, sigpos, sigvel):
		x = gauss(self.arr[0], sigpos)
		y = gauss(self.arr[1], sigpos)
		z = gauss(self.arr[2], sigpos)
		vx = gauss(self.arr[3], sigvel)
		vy = gauss(self.arr[4], sigvel)
		vz = gauss(self.arr[5], sigvel)
		self.arr = numpy.array([x, y, z, vx, vy, vz])

	def compute_orbit(self, disk_optn, bulge_optn, halo_optn):
		if(self.potential=='pointsrc'):
			self.orbit = inte.odeint(mf.PointSource, self.arr, self.t)

		if(self.potential=='wolfire'):
			self.orbit = inte.odeint(mf.WolfirePotential, self.arr, self.t, args=(disk_optn,bulge_optn,halo_optn))

	def write_file(self, filename):
		fn_head = 'x\ty\tz\tvx\tvy\tvz\n-\t-\t-\t--\t--\t--'
		to_write = numpy.savetxt(filename, self.orbit, delimiter='\t', header=fn_head, fmt='%.3f')


