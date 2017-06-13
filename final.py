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

def g(slice):	#g(wT yi)
	return 1.0 / (1.0 + np.exp(-1.0 * (np.dot(base, slice))))

def coef(x, y):	#the equation from the slides
	d = np.zeros((120,120))

	for slice in range(len(x[0])):
		yHat = g(x[slice])
		error = float(y[slice]) - yHat
		d = np.add(d, np.multiply(error, x[slice]))
	return d
	   
def threadStart(data,xLen,yLen,zLen,label):
	for z in range(zLen):
		ratio = (float(z*z_dim)/zLen)%1
		z1 = int(math.floor(z*z_dim/zLen))
		z2 = z1 + 1
		#sys.stdout.write("\rRunning... (" + str(z+1) + "/" + str(zLen) + ")")
		#sys.stdout.flush()	#real-time progress bar
		xThr = []
		for x in range(xLen):
			for y in range(yLen):
				base[x][y][z1] += (float)(data[z][x][y]) * (1-ratio)
				#coef(data[z],label)
				if(z2 < z_dim):
					base[x][y][z2] += (float)(data[z][x][y]) * ratio
	np.divide(base,zLen)
		
def learn(labels):
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
		
		thr.append(Process(target=threadStart,args=(data,xLen,yLen,zLen,labels[i][1])))
		thr[i].start()
		#threadStart(data,xLen,yLen,zLen)
		#end

	print "\nProcessing..."
		
	for i in range(fileLen):
		thr[i].join()
		sys.stdout.write("\rThread (" + str(i+1) + "/" + str(fileLen) + ") Complete")
		sys.stdout.flush()	#real-time progress bar
	
	#np.divide(base,fileLen)

def testSingle(label, num):
	acc = 0
	a = np.load("learn/"+fileNames[num],"r")
	for i in range(z_dim):
		for x in range(x_dim):
			if(round(a[x][x][i]) == label):
				acc += 1

	return float(acc) / float(z_dim)
	
labels = np.genfromtxt("stage1_labels.csv",delimiter=",")
#learn(labels)
print "\nAll Threads Complete"
#np.save("learn-set.npy", base)

base = np.load("learn-set.npy","r")

results = []
results.append([])
for i in range(fileLen):
	results.append([testSingle(labels[i][1],i),fileNames[i]])

out = open("results.csv","w")
out.write(str(results))
out.close()

#np.save("results.npy", results)
