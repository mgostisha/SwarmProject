import numpy
import pickle
import math
from random import gauss


def split_cols(f, n_columns, column):

    """ This function splits a 2D array with n number of columns 
    	into seperate 1D, 'row' arrays, one at a time. 

    n_columns refers to how many columns the array has
    column refers to which column you want, with 0 being the left-most column
    and (n_columns-1) being the right-most column
    """

    a = numpy.hsplit(f,n_columns)[column].reshape(-1)

    return a


def text2array(filename):

	""" This function takes a .txt file and turns it into an array of arrays. """
	""" This function is meant to be used for the SWARM website. """

	file_open = open(filename, 'r')

	header1 = file_open.readline()
	header2 = file_open.readline()
	columns = 7

	count = 0
	new_array = numpy.array([])

	for line in file_open:
		if(line != '' or line != '\n'):
			line=line.strip().split()
			new_array = numpy.append(new_array,line).astype(float)
			count += 1

	rows = count
	new_array = numpy.reshape(new_array, (rows,columns))

	file_open.close()

	return new_array


def out2file(arr, index):

	""" This function takes an array and outputs it to a .txt file """

	""" File name and File header string """

	fn = 'particle_' + str(index) + '.txt'
	fn_head = 'x\ty\tz\tvx\tvy\tvz\n-\t-\t-\t--\t--\t--'

	""" Write the array to a file """

	to_write = numpy.savetxt(fn, arr, delimiter='\t', header=fn_head, fmt='%.3f')
	print fn

def out2file_timesteps(arr, index):

	fn = 'timestep_' + str(index) + '.txt'
	fn_head = 'x\ty\tz\tvx\tvy\tvz\n-\t-\t-\t--\t--\t--'

	to_write = numpy.savetxt(fn, arr, delimiter='\t', header=fn_head, fmt='%.3f')
	print fn


def readResults(filename):

	""" This function takes an input file from the out2file function and
		creates a dictionary with the x, y, z, vx, vy, vz components.
	"""

	f = open(filename, 'r')
	header1 = f.readline()
	header2 = f.readline()

	x = numpy.array([])
	y = numpy.array([])
	z = numpy.array([])
	vx = numpy.array([])
	vy = numpy.array([])
	vz = numpy.array([])

	for line in f:
		line = line.strip().split()
		x = numpy.append(x,line[0])
		y = numpy.append(y,line[1])
		z = numpy.append(z,line[2])
		vx = numpy.append(vx,line[3])
		vy = numpy.append(vy,line[4])
		vz = numpy.append(vz,line[5])

	x = x.astype(float); y = y.astype(float); z = z.astype(float)
	vx = vx.astype(float); vy = vy.astype(float); vz = vz.astype(float)

	new_dict = {'x':x, 'y':y, 'z':z, 'vx':vx, 'vy':vy, 'vz':vz}

	f.close()

	return new_dict

def outputStyle(arr, option):

	""" This function is to be used with an array of arrays containing the orbits 
	of multiple particles from the simulation. It is written to be used with the 
	output array from test_solar.orbitFromFile, which has intricacies from using
	numpy's dstack() function. The array passed to this function should be 3D and 
	of size(timesteps, parameters, particles). """

	option = option.lower()

	"""if (option == "pkl"):
		with open(fn, 'w') as file:
			pickle.dump(arr, file)
	"""

	if (option == "orbits"):
		for i in range(1, len(arr[0,0,:])):
			out2file(arr[:,:,i], i-1)

	if (option == "timesteps"):
		temp_arr = numpy.array([])

		for i in range(len(arr)):
			for j in range(1, len(arr[0,0,:])):
				temp_arr = numpy.append(temp_arr, arr[:,:,j][i])
			temp_arr = numpy.reshape(temp_arr, (len(arr[0,0,:])-1,len(arr[0,:,0])))	
			out2file_timesteps(temp_arr, i)
			temp_arr = numpy.array([])

def createInitArr(x0, y0, z0, vx0, vy0, vz0, std_x, std_v, n_particles):

    tmp = numpy.array([])

    for i in range(n_particles):

        tmp = numpy.append(tmp,gauss(x0,std_x))
        tmp = numpy.append(tmp,gauss(y0,std_x))
        tmp = numpy.append(tmp,gauss(z0,std_x))
        tmp = numpy.append(tmp,gauss(vx0,std_v))
        tmp = numpy.append(tmp,gauss(vy0,std_v))
        tmp = numpy.append(tmp,gauss(vz0,std_v))

    tmp = tmp.reshape(n_particles,6)

    return tmp

def computeCourantTime(dx, dy, dz, vx, vy, vz, C):

	""" Computes the Courant Timestep Value for adaptive timesteps. Positions should"""
	""" be in kpc and velocities should be in km/s. C is the constant for which fraction"""
	""" of the maximum timestep is wanted. """

	"""Conversion of velocities to kpc/Gyr (1 km/s = 1.023 kpc/Gyr)"""
	"""and absolute values of the length interval """

	dx = math.fabs(dx)
	dy = math.fabs(dy)
	dz = math.fabs(dz)
	vx = math.fabs(1.023*vx)
	vy = math.fabs(1.023*vy)
	vz = math.fabs(1.023*vz)

	""" Make sure velocities are non-zero"""

	if (math.fabs(vx) == 0.0):
		vx = 0.01
	if (math.fabs(vy) == 0.0):
		vy = 0.01
	if (math.fabs(vz) == 0.0):
		vz = 0.01

	print vx, vy, vz

	tstep = C*(dx/vx + dy/vy + dz/vz)

	return tstep

def dragParameters(vfield, denfield, vzero, vRsc, nHcen, nHcen2, Rscpow, alphapow, nHdisk1, Rscdisk1, Zscdisk1,
	nHdisk2, Rscdisk2, Zscdisk2, nHdisk3, Rscdisk3, Zscdisk3):

	""" Decision function to decide which drag parameters should be used in the simulation. """

	rhoparams = []
	velparams = []

	# Get velocity field choice and put parameters into list
	if (vfield == 'voutflow'):
		velparams.append(vzero)
		if(vRsc != 0.0):
			velparams.append(vRsc)
		else:
			velparams.append(1.0)

	# Get density field choice and put parameters into list
	if (denfield == 'constantrho'):
		rhoparams.append(nHcen)
	elif (denfield == 'powerlawrho'):
		rhoparams.append(nHcen2)
		if(Rscpow != 0.0):
			rhoparams.append(Rscpow)
		else:
			rhoparams.append(1.0)
		rhoparams.append(alphapow)
	elif (denfield == 'disks'):
		if (Rscdisk1 != 0.0 and Zscdisk1 != 0.0):
			rhoparams.append(nHdisk1)
			rhoparams.append(Rscdisk1)
			rhoparams.append(Zscdisk1)
		if (Rscdisk2 != 0.0 and Zscdisk2 != 0.0):
			rhoparams.append(nHdisk2)
			rhoparams.append(Rscdisk2)
			rhoparams.append(Zscdisk2)
		if (Rscdisk3 != 0.0 and Zscdisk3 != 0.0):
			rhoparams.append(nHdisk3)
			rhoparams.append(Rscdisk3)
			rhoparams.append(Zscdisk3)

	return rhoparams, velparams

def computeDrag(params, vfield, denfield, r, vr, gr, z, vz, N_c):

	""" Takes the parameter array from the reduction function and additional internal parameters for the potential
	match velocity field and calculates the drag. """

	denparams = params[0]
	velparams = params[1]
	C_D = 1.0

	if (vfield == 'zerov'):
		v = 0.0
	elif (vfield == 'potentialmatch'):
		v = math.sqrt(r * math.fabs(gr))
	elif (vfield == 'voutflow'):
		v = velparams[0] * r / velparams[1]

	if (denfield == 'constantrho'):
		nH = denparams[0]
	elif (denfield == 'powerlawrho'):
		nH = denparams[0]/((1 + (r / denparams[1])**2)**denparams[2])
	elif (denfield == 'disks'):
		nH = 0.0
		for i in range(0, len(rhoparams), 3):
			nH += denparams[i] * math.pow(numpy.e, -r/denparams[i+1]) * math.pow(numpy.e, -z/denparams[i+2])

	adr = -C_D/(2.0*N_c) * nH * math.fabs(vr - v) * (vr - v)
	adz = -C_D/(2.0*N_c) * nH * math.fabs(vz - 0.0) * (vz - 0.0)

	return adr, adz






    
