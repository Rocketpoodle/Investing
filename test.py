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
for i in range(0,random.randrange(10,21)):
    x = random.random()*50
    y = random.random()*50
    d = 10 + random.random()*20
    for j in range(0,random.randrange(10,51)):
        data1.appendDataPoint([x + d*random.random(), y + d*random.random()])
data1.plotData("x",["y"], scatter = [True], blocking=False)
kmeans, sil, DI, DB = data1.kmeanAnalysis()
if DB != 0:
    print(sil, DI, DB, DI*sil / DB)
rawkmeans, sil, DI, DB = data1.kmeanAnalysis(refine=False)
if DB != 0:
    print(sil, DI, DB, DI*sil / DB)
trimkmeans, sil, DI, DB = data1.kmeanAnalysis(trim=True)
if DB != 0:
    print(sil, DI, DB, DI*sil / DB)
end = time.time()
print(len(kmeans), end - start)
xarr = []
yarr = []
print(len(kmeans))
for point in kmeans:
    xarr.append(point[0][0])
    yarr.append(point[0][1])
plt.scatter(xarr, yarr, marker='x')
xarr = []
yarr = []
print(len(rawkmeans))
for point in rawkmeans:
    xarr.append(point[0][0])
    yarr.append(point[0][1])
plt.scatter(xarr, yarr, marker='x')
xarr = []
yarr = []
print(len(trimkmeans))
for point in trimkmeans:
    xarr.append(point[0][0])
    yarr.append(point[0][1])
plt.scatter(xarr, yarr, marker='+')
for point in kmeans:
    plt.subplot().add_artist(plt.Circle(point[0],4*point[1],fill=False))
plt.show()
#print(kmeans)
print(len(kmeans))