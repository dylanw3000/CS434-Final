import numpy as np
import scipy
import os
import math
import sys

from multiprocessing import Process

x_dim = 120;
y_dim = 120;
z_dim = 120;

base = np.zeros((x_dim,y_dim,z_dim))

fileNames = os.listdir("learn")
fileLen = len(fileNames)

def threadStart(data,xLen,yLen,zLen):
	for z in range(zLen):
		ratio = (float(z*z_dim)/zLen)%1
		z1 = int(math.floor(z*z_dim/zLen))
		z2 = z1 + 1
		#sys.stdout.write("\rRunning... (" + str(z+1) + "/" + str(zLen) + ")")
		#sys.stdout.flush()	#real-time progress bar
		xThr = []
		for x in range(xLen):
			for y in range(yLen):
				base[x][y][z1] += data[z][x][y] * (1-ratio)
				if(z2 < z_dim):
					base[x][y][z2] += data[z][x][y] * ratio
		
def learn():
	thr = []

	for i in range(fileLen):
		data = np.load("learn/" + fileNames[i], "r")

		sys.stdout.write("\rInitilizing Thread (" + str(i+1) + "/" + str(fileLen) + ")")
		sys.stdout.flush()	#real-time progress bar

		zLen = len(data)
		xLen = len(data[0])
		yLen = len(data[0][0])
		
		"""
		print xLen
		print yLen
		print zLen
		"""
		
		thr.append(Process(target=threadStart,args=(data,xLen,yLen,zLen)))
		thr[i].start()
		#end

	print "\nProcessing..."
		
	for i in range(fileLen):
		thr[i].join()
		sys.stdout.write("\rThread (" + str(i+1) + "/" + str(fileLen) + ") Complete")
		sys.stdout.flush()	#real-time progress bar
	
	np.divide(base,fileLen)

learn()
print "\nAll Threads Complete"
