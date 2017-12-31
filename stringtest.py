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
movavg = 0
lastmovavg = 0
endrange = 100
for i in range(0,1000):
    data1 = DataSet(["x","y"])
    y = random.randrange(-100,100)
    avaar = []
    for x in range(0,endrange+1):
        y += random.randrange(-50,51)
        if x > 4:
            lastmovavg = movavg
            movavg = data1.getMovAvg("y",5)
        else:
            movavg = y
        data1.appendDataPoint([x,y])
        avaar.append(movavg)     
    fitname, fit, rsq = data1.getCurveFitEasy("x","y")
    minmax = fit.getMinMax([0,51], scale = True)
    kmeans = data1.getKmeans("y")
    stats = data1.getStats("y")
    data1.addDataVariable("kl", [kmeans[0][0]]*data1.lenData + kmeans[0][1])
    data1.addDataVariable("kh", [kmeans[1][0]]*data1.lenData - kmeans[1][1])
    data1.addDataVariable("mvav", avaar)
    arsq += rsq
    deg += fit.degree
    yvals = data1.getDataVariable("y")
    deriv = fit.differentiate().evaluate(endrange-1,scale=True)
    print(fit.degree, rsq)
    print(kmeans)
    print(stats)
    print(movavg)
    print(minmax)
    print(yvals[endrange] - yvals[endrange-1], deriv, movavg - lastmovavg)
    data1.plotData("x",["y",fitname,"kl","kh"])
    print("")
arsq /= 1000
deg /= 1000
end = time.time()
total = end - start
print("Time Elapsed: ", total, "\nTime per: ", (total/1000))
print(arsq, deg)
