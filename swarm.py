import urllib as url
import zipfile as zippy
import numpy 
import glob
import os
from matplotlib import rc, rcParams
from pylab import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def getZip(fileID):

	""" This function takes the number, or file ID (as a string) of the zip file produced by swarm and """
	""" Retrieves it from the web, unzips it, and puts the .txt files in a directory. """

	fileID = str(fileID).zfill(5)

	url.urlretrieve("http://www.astro.wisc.edu/~gostisha/resource/download/swarm/swarm_"+fileID+".zip", "swarm.zip")

	z = zippy.ZipFile("swarm.zip")
	z.extractall(fileID+"/")
	z.close()

	print "There is now a directory named "+fileID+"/ containing the swarm text files."

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
	columns = len(header1.strip().split())-1

	count = 0
	new_array = numpy.array([])

	for line in file_open:
		line=line.strip().split()
		new_array = numpy.append(new_array,line).astype(float)
		count += 1

	rows = count
	new_array = numpy.reshape(new_array, (rows,columns))

	file_open.close()

	return new_array

def text2dict(filename):

	""" This function takes a .txt file and turns it into an array of arrays. """
	""" This function is meant to be used for the SWARM website """

	x, y, z, vx, vy, vz = numpy.loadtxt(filename, delimiter='\t', skiprows=2, unpack=True)

	new_dict = {'x':x, 'y':y, 'z':z, 'vx':vx, 'vy':vy, 'vz':vz}

	return new_dict

def allFileDict(filedir):

	""" This function takes a directory with all of the swarm result files in it. The argument filedir """
	""" Should be a string. Then, it makes a dictionary containing the phase space values of each particle """
	""" Or timestep, and puts them all into a giant list, therefore returning a data structure with all """
	""" Of the results from the swarm calculation. """

	filenames = []
	finallist = []
	globkey = filedir+"/*.txt"

	for files in glob.glob(globkey):
		filenames.append(files)

	for i in range(len(filenames)):
		print "Unpacking: " + str(i)
		tempdict = text2dict(filenames[i])
		finallist.append(tempdict)

	return finallist

def getData(fileID):

	fileID = str(fileID).zfill(5)

	getZip(fileID)
	final = allFileDict(fileID)

	return final

def plotData(dictlist, xkey, ykey):

	"""rc('text', usetex=True)"""
	"""rc('font', **{'family':'serif', 'serif':['Computer Modern']})"""

	plt.axes().set_aspect('equal')
	plt.ylabel(ykey+' (pc)')
	plt.xlabel(xkey+' (pc)')
	plt.title('Orbits')

	for i in range(size(dictlist)):
		plt.plot(dictlist[i][xkey], dictlist[i][ykey])

	plt.show(block=False)

def plotData3D(dictlist, xkey, ykey, zkey):

	fig = figure()
	ax = Axes3D(fig)
	ax.set_xlabel(xkey+' (pc)')
	ax.set_ylabel(ykey+' (pc)')
	ax.set_zlabel(zkey+' (pc)')
	plt.title('Orbits')

	for i in range(size(dictlist)):
		plt.plot(dictlist[i][xkey], dictlist[i][ykey], dictlist[i][zkey])

	plt.show(block=False)

def orbitAnimate(dictlist, xkey, ykey):
    
    fig, ax = plt.subplots()
    plt.plot((0), marker='o', linestyle='None')
    plt.ylabel(ykey+' (pc)')
    plt.xlabel(xkey+' (pc)')
    plt.title('Orbit Animation')

    minx = min([min(dictlist[i][xkey]) for i in range(len(dictlist))]) + 500.0
    miny = min([min(dictlist[i][ykey]) for i in range(len(dictlist))]) + 500.0
    maxx = max([max(dictlist[i][xkey]) for i in range(len(dictlist))]) + 500.0
    maxy = max([max(dictlist[i][ykey]) for i in range(len(dictlist))]) + 500.0

    waittime = 10./len(dictlist[0]['x'])

    for t in range(len(dictlist[0][xkey])):
        if t == 0:
            points, = ax.plot((dictlist[0][xkey][t], dictlist[0][ykey][t]), marker='o', linestyle='None')
            ax.set_xlim(minx,maxx)
            ax.set_ylim(miny,maxy)
            axes().set_aspect('equal')
            raw_input('Press enter to run animation...')
        else:
            new_x = []; new_y = [];
            for j in range(size(dictlist)):
                new_x.append(dictlist[j][xkey][t])
                new_y.append(dictlist[j][ykey][t])
            points.set_data((new_x, new_y))
        plt.pause(waittime)

def timestep_files(filedir):

 	filenames = []
 	arrlist = []
 	globkey = filedir+'/*.txt'
 	fn_head = 'x\ty\tz\tvx\tvy\tvz\n-\t-\t-\t--\t--\t--'

 	for files in glob.glob(globkey):
 		filenames.append(files)

 	for i in range(len(filenames)):
 		temparr = text2array(filenames[i])
 		arrlist.append(temparr)

	for i in range(len(arrlist[0])):
		output_fn = filedir+'/timestep_'+str(i)+'.txt'
		temparr = []

 		for j in range(len(arrlist)):
 			temparr = numpy.append(temparr, arrlist[j][i])
 			temparr = numpy.array(temparr)
 			#print temparr

 		temparr = numpy.reshape(temparr, (len(filenames), len(arrlist[0][0])))
 		to_write = numpy.savetxt(output_fn, temparr, delimiter='\t', header = fn_head, fmt = '%.3f')
 		print 'Finished: Timestep '+str(i)

 	delete_old = raw_input('Do you want to delete the old particle files? Enter yes or no.\n')
 	delete_old.lower()

 	if (delete_old == 'yes'):
 		cmd = 'rm '+filedir+'/particle_*.txt'
 		os.system(cmd)







			










