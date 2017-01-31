__author__ = 'Austin'
from DataSet import *
import numpy as np
from Polynomial import *
import random
import time
import cmath


data1 = DataSet(["x","y"])
end = random.randrange(10,20)
end2 = random.randrange(2,8)
for x in range (0,end):
    eval = random.randrange(-10,10)
    for y in range(0,end2):
        eval2 = random.randrange(-2,2)
        data1.appendDataPoint([((x*end2)+y),eval+eval2+100])
scale, offset = data1.scaleDataVariable("x")
print(scale)
fit,rsq = data1.curveFit("x","y")
dp = fit.differentiate()
ddp = dp.differentiate()
coeffarr = dp.getRoots(real=True)
coeffarr.sort(reverse=True)
mins = []
for elements in coeffarr:
    if ddp.evaluate(elements) > 0 and elements <= 1 and elements >= 0:
        mins.append(elements)
if len(mins) > 0:
    print(mins[0])
fitdata = fit.evaluate(data1.getDataVariable("x"))
data1.addDataVariable("fit",fitdata)
data1.plotData("x",["y","fit"],iscale = scale, ioffset = offset)