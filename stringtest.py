__author__ = 'Austin'
from DataSet import *
import numpy as np
from Polynomial import *
import random
import time
import cmath


data1 = DataSet(["x","y"])
"""
genpoly = Polynomial([1,-5,-50,50])
fracterr = 0.5
for x in range(-7,14):
    error = 1 + fracterr*random.randrange(-1,1)
    value = genpoly.evaluate(x)*error
    data1.appendDataPoint([x,value])
"""
y = random.randrange(-10,10)
for x in range(0,50):
    y += random.randrange(-2,2)
    data1.appendDataPoint([x,y])
data1.scaleDataVariable("x")
fit,rsq = data1.curveFit("x","y")
print(fit.degree)
dp = fit.differentiate()
ddp = dp.differentiate()
coeffarr = dp.getRoots(real=True)
coeffarr.sort(reverse=True)
mins = []
for elements in coeffarr:
    if ddp.evaluate(elements) > 0 and elements <= 0 and elements >= 0:
        mins.append(elements)
if len(mins) > 0:
    print(mins[0])
fitdata = fit.evaluate(data1.getDataVariable("x"))
data1.addDataVariable("fit",fitdata)
#data1.plotData("x",["y","fit"])
data1.plotData("x",["y","fit"], scaled = False)


