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
    for x in range(0,50):
        y += random.randrange(-5,6)
        data1.appendDataPoint([x,y])
    data1.scaleDataVariable("x")
    fit,rsq = data1.curveFit("x","y")
    minmax = fit.getMinMax(interval = [0,1])
    kmeans = data1.getKmeans("y")
    stats = data1.getStats("y")
    movavg = data1.getMovAvg("y",5)
    fitdata = fit.evaluate(data1.getDataVariable("x"))
    data1.addDataVariable("fit",fitdata)
    data1.addDataVariable("kl", [kmeans[0][0]]*data1.lenData)
    data1.addDataVariable("kh", [kmeans[1][0]]*data1.lenData)
    arsq += rsq
    deg += fit.degree
    print(fit.degree, rsq)
    #print(kmeans)
    #print(stats)
    #print(movavg)
    print(minmax)
    data1.plotData("x",["y","fit","kl","kh"])
arsq /= 1000
deg /= 1000
end = time.time()
total = end - start
print("Time Elapsed: ", total, "\nTime per: ", (total/1000))
print(arsq, deg)
