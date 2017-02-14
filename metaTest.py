from abc import ABCMeta, abstractmethod
import time
class DataPoint():

    def getDataArray(self):
        attributes = self.__dict__
        vals = []
        for key in attributes:
            vals.append(attributes[key])
        return vals

    def getNameArray(self):
        attributes = self.__dict__
        names = []
        for key in attributes:
            names.append(key)
        return names

StockData = type('StockData', (DataPoint,), {})

newpoint = StockData()
newpoint.x = 1

newpoint.y = 2
newpoint.z = 3
newpoint.w = 4
newpoint.a = 5
newpoint.b = 6
newpoint.c = 7

newpoint.d = 8

print(newpoint.x)

x = []
y = []
z = []
w = []
start = time.time()
for i in range(0, 100000):
    B = newpoint.getDataArray()

    x.append(B[0])
    y.append(B[1])
    z.append(B[2])
    w.append(B[3])
    x.append(B[4])
    y.append(B[5])
    z.append(B[6])
    w.append(B[7])

print(time.time() - start)