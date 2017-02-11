import math
import numpy
import random
import matplotlib.pyplot as plt    
from DataSet import *
import time

start = time.time()
data1 = DataSet(["x","y"])
for x in range(0,1000,10):
    for y in range(0,10):
        data1.appendDataPoint([random.random()*1008, random.random()*1008])
        #data1.appendDataPoint([x + 8*random.random(),x + 8*random.random()])
data1.plotData("x",["y"], scatter = [True], blocking=False)
kmeans, DB, DI, SIL = data1.kmeanAnalysis(sigmaScale=3)

end = time.time()
print(len(kmeans), end - start)
xarr = []
yarr = []
print(kmeans)
for point in kmeans:
    xarr.append(point[0][0])
    yarr.append(point[0][1])
plt.scatter(xarr, yarr, marker='x')
plt.show()
#print(kmeans)
print(len(kmeans))