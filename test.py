import math
import numpy
import random
import matplotlib.pyplot as plt    
from DataSet import *
import time

start = time.time()
data1 = DataSet(["x","y"])
#for x in range(0,50):
#        data1.appendDataPoint([random.random()*50, random.random()*50])
print("numMeans, donecheck, composite, DI, DB, sil")
for i in range(0,random.randrange(2,11)):
    x = random.random()*50
    y = random.random()*50
    d = random.random()*40
    for j in range(0,random.randrange(10,51)):
        data1.appendDataPoint([x + d*random.random(), y + d*random.random()])
data1.plotData("x",["y"], scatter = [True], blocking=False)
kmeans, oldMeans = data1.kmeanAnalysis()

end = time.time()
print(len(kmeans[0]), end - start)
xarr = []
yarr = []
print(kmeans[0])
for point in kmeans[0]:
    xarr.append(point[0][0])
    yarr.append(point[0][1])
plt.scatter(xarr, yarr, marker='x')
xarr = []
yarr = []
print(oldMeans[0])
for point in oldMeans[0]:
    xarr.append(point[0][0])
    yarr.append(point[0][1])
plt.scatter(xarr, yarr, marker='x')
plt.show()
#print(kmeans)
print(len(kmeans))