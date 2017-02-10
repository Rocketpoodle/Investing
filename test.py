import math
import numpy
import random
import matplotlib.pyplot as plt    
from DataSet import *

data1 = DataSet(["x","y"])
for x in range(0,50,10):
    for y in range(0,10):
        data1.appendDataPoint([x + 9*random.random(),x + 9*random.random()])
data1.plotData("x",["y"], scatter = [True], blocking = False)
kmeans, same = data1.kmeanAnalysis(2)
xarr = []
yarr = []
for point in kmeans:
    print(point)
    xarr.append(point[0][0])
    yarr.append(point[0][1])
plt.scatter(xarr, yarr)
plt.show()
#print(kmeans)
print(len(kmeans[0]))