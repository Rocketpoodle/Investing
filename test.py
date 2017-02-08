import math
import numpy
import random
import matplotlib.pyplot as plt    
from DataSet import *

data1 = DataSet(["x","y"])
for x in range(0,101,10):
    for y in range(0,10):
        data1.appendDataPoint([x + 5*random.random(),x + 5*random.random()])
data1.plotData("x",["y"], scatter = [True])
kmeans = data1.kmeanAnalysis(2)
print(kmeans)
print(len(kmeans[0]))