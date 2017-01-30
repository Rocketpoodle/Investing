__author__ = 'Austin'
from DataSet import *
import numpy as np
from Polynomial import *
import random
import time


data1 = DataSet(["x","y"])
end = random.randrange(10,20)
end2 = random.randrange(2,8)
for x in range (0,end):
    eval = random.randrange(-10,10)
    for y in range(0,end2):
        eval2 = random.randrange(-2,2)
        data1.appendDataPoint([((x*end2)+y),eval+eval2])
kmeans = data1.getKmeans("y")
kh = []
kl = []
for x in range(0, data1.lenData):
    kh.append(kmeans[1][0])
    kl.append(kmeans[0][0])
data1.addDataVariable("kh",kh)
data1.addDataVariable("kl",kl)
data1.plotData("x",["kh","kl","y"])
