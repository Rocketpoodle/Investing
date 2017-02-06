__author__ = 'Austin'
from DataSet import *
import numpy as np
from Polynomial import *
import random
import time
import cmath


min = None
start = time.time()
arsq = 0
deg = 0
for i in range(0,1000):
    data1 = DataSet(["x","y"])
    y = random.randrange(-10,10)
    for x in range(0,51):
        y += random.randrange(-5,6)
        data1.appendDataPoint([x,y])
    fitname, fit, rsq = data1.getCurveFitEasy("x","y")
    minmax = fit.getMinMax([0,51], scale = True)
    kmeans = data1.getKmeans("y")
    stats = data1.getStats("y")
    movavg = data1.getMovAvg("y",5)
    data1.addDataVariable("kl", [kmeans[0][0]]*data1.lenData)
    data1.addDataVariable("kh", [kmeans[1][0]]*data1.lenData)
    arsq += rsq
    deg += fit.degree
    print(fit.degree, rsq)
    print(kmeans)
    print(stats)
    print(movavg)
    print(minmax)
    data1.plotData("x",["y",fitname,"kl","kh"], scaled = True)
arsq /= 1000
deg /= 1000
end = time.time()
total = end - start
print("Time Elapsed: ", total, "\nTime per: ", (total/1000))
print(arsq, deg)
