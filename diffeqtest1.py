from Polynomial import *
from DataSet import *

data1 = DataSet(["t"])

mass = 10
target = 5
force = 1.5
startd = 0
startv = 0



t = []
incr = 0
for x in range(0, 51):
    t.append(incr)
    incr += 1
    data1.appendDataPoint([incr])

y = []
current = startd
velocity = startv
for x in range(0, 51):
    y.append(current)
    velocity += (target - current)
    current += velocity
    print(target, current, velocity)
data1.addDataVariable("x", y)

y = []
current = startd
velocity = startv
lastd = startd
integral = 0
for x in range(0,51):
    y.append(current)
    integral += (target - current)
    differential = (target - current) - lastd
    lastd = (target - current)
    pid = (target - current) + differential + integral
    velocity = pid
    current += velocity*0.00001
data1.addDataVariable("y", y)

data1.plotData("t", ["x", "y"],scaled=False)