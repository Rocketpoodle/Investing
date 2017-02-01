__author__ = 'Austin'
from DataSet import *
import numpy as np
from Polynomial import *
import random
import time
import cmath

"""
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
    if fit.degree > 1:
        dp = fit.differentiate()
        ddp = dp.differentiate()
        coeffarr = dp.getRoots(real=True)
        coeffarr.sort(reverse=True)
        mins = []
        for elements in coeffarr:
            if ddp.evaluate(elements) > 0 and elements <= 1 and elements >= 0:
                mins.append(elements)
        if len(mins) > 0:
            min = (mins[0] - data1.varOffset[0])*data1.varScale[0]
    kmeans = data1.getKmeans("y")
    stats = data1.getStats("y")
    movavg = data1.getMovAvg("y",5)
    fitdata = fit.evaluate(data1.getDataVariable("x"))
    data1.addDataVariable("fit",fitdata)
    arsq += rsq
    deg += fit.degree
    print(fit.degree, rsq)
    data1.plotData("x",["y","fit"],scaled = False)
arsq /= 1000
deg /= 1000
end = time.time()
total = end - start
print("Time Elapsed: ", total, "\nTime per: ", (total/1000))
print(kmeans)
print(stats)
print(movavg)
print(min)
print(arsq, deg)
"""
poly = Polynomial([2,1])
integral = poly.integrate()
print(poly)
print(integral)
integral = poly.integrate(offset = 3)
print(integral)
integral = poly.integrate(initialvalue = [2,5])
print(integral)
integral = poly.integrate(interval = [2,5])
print(integral)