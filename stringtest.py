__author__ = 'Austin'
from DataSet import *
import numpy as np
from Polynomial import *
import random
import time

start = time.time()
bestdata = None
bestrsq = 0
avrsq = 0
for i in range(0,1000):
    data1 = DataSet(["x","y"])
    end = random.randrange(10,20)
    end2 = random.randrange(2,8)
    for x in range (0,end):
        eval = random.randrange(-10,10)
        for y in range(0,end2):
            eval2 = random.randrange(-2,2)
            data1.appendDataPoint([((x*end2)+y),eval+eval2])
    data1.scaleDataVariable("x")
    #data1.scaleDataVariable("y")
    fit,rsq = data1.curveFit("x","y")
    print(rsq)
    fitdata = fit.evaluate(data1.getDataVariable("x"))
    data1.addDataVariable("fit",fitdata)
    data1.plotData("x",["y","fit"])
    if rsq > bestrsq:
        bestdata = data1
        bestrsq = rsq
end = time.time()
print(avrsq / 1000)