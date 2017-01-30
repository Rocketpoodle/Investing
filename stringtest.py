__author__ = 'Austin'
from DataSet import *
import numpy as np
from Polynomial import *
import random


data1 = DataSet(["x","y"])
end = random.randrange(2,8)
end2 = random.randrange(2,8)
for x in range (0,end):
    eval = random.randrange(-10,10)
    for y in range(0,end2):
        eval2 = random.randrange(-2,2)
        data1.appendDataPoint([((x*end2)+y),eval+eval2])
fit,rsq = data1.curveFit("y","x")
print(fit, rsq)
polyData = fit.evaluate(data1.getDataVariable("x"))
data1.addDataVariable("fit", polyData)
data1.plotData("x", ["y","fit"])