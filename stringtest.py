__author__ = 'Austin'
from DataSet import *
import numpy as np
from Polynomial import *

data1 = DataSet(["x","y"])
data1.appendDataPoint([1,2])
data1.appendDataPoint([6,3],["y","x"])
data1.insertDataPoint([2,4],1)
print(data1)
mat2 = data1.toMatrix(vars = "y")
mat1 = []
col = []
for x in range(0, data1.lenData):
    col.append(1)
mat1.append(col)
mat1.append(data1.data[0])
mat1 = np.matrix(mat1)
mat3 = mat1.transpose()
print(mat1)
print(mat2)
mat2 = mat1*mat2
mat1 = mat1*mat3
print(mat1)
print(mat2)
solution = np.linalg.qr(mat1)
print(solution)
done = np.linalg.solve(mat1,mat2)
print(done)
coeffs = []
for x in range(0, 2):
    coeffs.append(done.item(x))
coeffs.reverse()
poly = Polynomial(coeffs)
print(poly)
