import numpy as np
import matplotlib.pyplot as plt
from Polynomial import *
import math

class DataSet(object):
    """Data set is an object that holds datasets
       data must be of equal length"""
    
    dataNames = [] # holds string data names for data members
    data = [] # array of data arrays. Primary array index corresponds to data name index
    numVars = 0 # number of data variables (data sub arrays)
    lenData = 0 # length of data sub arrays

    def __init__(self, dataNames = None, data = None):
        # check for data names present
        if dataNames != None: 
            self.dataNames = dataNames
            self.numVars = len(dataNames)
            for x in range(0, self.numVars): # verify no duplicate data names
                if(self.dataNames.count(self.dataNames[x]) != 1):
                    raise ValueError("Duplicate data name found")
        else:
            self.dataNames = []
            self.numVars = 0
        # check if data is present
        if data != None:
            # check for all variables accounted for
            if self.numVars != len(data):
                raise ValueError("Data set size doesn't match number of variables")
            self.data = data
            self.lenData = 0
            length = 0
            for x in range(0, self.numVars):
                if type(data[0]) == list: # make sure member is a list
                    length = len(data[0])
                else:
                    raise ValueError("Data should be array of arrays of same length")
                if self.lenData == len: # make sure length matches
                    self.lenData = len
                else:
                    raise ValueError("Data sub array lengths must be the same size")
        else: # if data is not given then it creates array of empty arrays
            self.data = []
            for x in range(0, self.numVars):
                self.data.append([])

    def appendDataPoint(self, pointData, pointNames = None):
        """appends datapoint to array with optional names array"""
        if len(pointData) != self.numVars: # check for proper point size
            raise ValueError("data point has incorrect number of values")
        if pointNames != None:
            for x in range(0, self.numVars): # verify no duplicate data names
                if(pointNames.count(pointNames[x]) != 1):
                        raise ValueError("Duplicate data name found")
            swaparr = []
            for x in range(0,self.numVars): # swap data to correct position
                swaparr.append(pointData[pointNames.index(self.dataNames[x])])
            pointData = swaparr
        for x in range(0,self.numVars): # append new data
            self.data[x].append(pointData[x])
        self.lenData += 1 # increment index

    def insertDataPoint(self, pointData, index, pointNames = None):
        """inserts datapoint into array at index with optional names array"""
        if len(pointData) != self.numVars: # check for proper point size
            raise ValueError("data point has incorrect number of values")
        if pointNames != None:
            for x in range(0, self.numVars): # verify no duplicate data names
                if(pointNames.count(pointNames[x]) != 1):
                    raise ValueError("Duplicate data name found")
            swaparr = []
            for x in range(0, self.numVars): # swap data to correct position
                swapvar.append(pointData[pointNames.index(self.dataNames[x])])
            pointData = swaparr
        for x in range(0, self.numVars): # insert new data
            self.data[x].insert(index, pointData[x])
        self.lenData += 1 # increment index

    def popDataPoint(self, index = None, independant = None):
        """pops data point at index (none pops last data point)
        optional independant to use as index"""
        popped = []
        if index != None: # check if index is given
            if independant != None: # checks if independant var is given
                index = self.data[self.dataNames.index(independant)].index(index) # get index of value from variable independant
            for x in range(0, self.numVars): # pop data
                self.data[x].pop(index)
        else:
            for x in range(0, self.numVars): # pop data
                popped.append(self.data[x].pop())
        self.lenData -= 1 # decrement length
        return popped

    def addDataVariable(self, varName, varData):
        """adds variable to dataset (requires data of length equal to current data length)"""
        if self.dataNames.count(varName) != 0: # check if variable already exists
            raise ValueError("A variable of that name already exists")
        if self.lenData != len(varData): # check that data is same length
            raise ValueError("New data is not of the correct length")
        self.data.append(varData) # append variable
        self.dataNames.append(varName)
        self.numVars += 1 # increment number of variables

    def delDataVariable(self, varName):
        """removes variable from dataset"""
        if self.dataNames.count(varName) == 0: # check if variable already exists
            raise ValueError("Variable not found")
        self.numVars -= 1 # decrement variable
        popindex = self.dataNames.index(varName)
        self.dataNames.pop(popindex)
        return self.data.pop(popindex) # pop variable

    def getDataPoint(self, index, vars = None, varName = None):
        """returns datapoint at index. Can specify variable name to use as index (only returns first occurance of index)
        can specify variables to return"""
        point = []
        if varName != None: # check if given variable name    
            if self.dataNames.count(varName) == 0: # check if variable already exists
                raise ValueError("Variable not found")
            index = self.dataNames.index(varName)
        for x in range(0, self.numVars): # get data point
            point.append(self.data[x][index])
        if vars != None: # change to return specified
            swappoint = []
            for names in vars:
                swappoint.append(point[self.dataNames.index(names)]) # swap data
            point = swappoint
        return point

    def getDataVariable(self, varName):
        """gets data array for varname"""
        return self.data[self.dataNames.index(varName)].copy()

    def toMatrix(self, vars = None, swap = False):
        """returns dataset in numpy matrix form. can specify which variables to use and wether to swap rows and columns"""
        mat = []
        if vars != None:
            for names in vars: # format matrix
                mat.append(self.data[self.dataNames.index(names)])
        else: #default format
            mat = self.data
        mat = np.matrix(mat) # create matrix
        if not swap: # invert if desired
            mat = mat.transpose()
        return mat

    def scaleDataVariable(self, varName, start = 0, end = 1):
        """scales vales to range from start to end"""
        index = self.dataNames.index(varName)
        scale = end - start
        if self.lenData == 0 or scale == 0: # check for empty data or 0 scale
            return None
        minval, maxval = self.getMinMax(varName)
        scale *= (maxval - minval)
        start -= minval
        for x in range(0,self.lenData): # scale values
            newval = (start + self.data[index][x]) / scale
            self.data[index][x] = newval
        return scale, start

    def plotData(self, independant, dependant, iscale = 1, ioffset = 0, dscale = None, doff = None, blocking = True):
        """plots data of dataset, specifying name of independant variable and dependant variable(s).
        can specify plot arguments"""
        scalar = [1] * self.numVars
        offset = [0] * self.numVars
        if dscale != None: # check for scale
            if len(dscale) != len(dependant):
                raise ValueError("incorrect size of scale array")
            for names in dependant: # copy scale and offset values
                scalar[self.dataNames.index(names)] = dscale[dependant.index(names)]
        if doff != None: # check for scale
            if len(doff) != len(dependant):
                raise ValueError("incorrect size of doff array")
            for names in dependant: # copy offset values
                offset[self.dataNames.index(names)] = doff[dependant.index(names)]
        xVals = [(x*iscale) + ioffset for x in self.data[self.dataNames.index(independant)]]
        for names in dependant: # plot data according to specification
            index = self.dataNames.index(names)
            plt.plot(xVals,[(x*scalar[index]) - offset[index] for x in self.data[index]])
        plt.show(block=blocking) # show plot

    def curveFit(self, independant, dependant, degree = None):
        """returns curve fit of requested data. Can specify degree or quality factor.
        If no degree is specified it finds the best degree using quality factor"""
        depIndex = self.dataNames.index(dependant) # get index for dependant variable
        indepIndex = self.dataNames.index(independant) # get index for independant variable
        if len(set(self.data[indepIndex])) != self.lenData: # duplicate independant values
               raise ValueError("Independant variable set contains duplicates")
        yval = self.data[depIndex].copy() # get yi
        ymean = 0
        for x in range(0, self.lenData):
            ymean += yval[x]
        ymean /= self.lenData # get mean of y values
        syi = 0
        for x in range (0, self.lenData): # get sum squares of ydistance
            dist = (yval[x] - ymean)
            dist *= dist
            syi += dist
        AT = []
        matB = self.toMatrix(vars = dependant)
        currArr = [1]*self.lenData # create initial row
        AT.append(currArr)
        currArr = self.data[indepIndex].copy() # get independant variable data
        AT.append(currArr)
        rSquared = 0
        lastrsq = 0
        poly = None
        lastpoly = None
        lasteval = None
        diff = 1
        eval = [0] * self.lenData
        polyArr = []
        if degree == None: # check if degree is given
            degree = self.lenData - 1# past 15 error is too high
            # iterative solution
            for x in range(1,degree):
                matAT = np.matrix(AT) # get Atranspose
                matA = matAT.transpose()
                matLU = matAT * matA # Atranspose * A
                matBx = matAT * matB # Atranspose * B
                done = np.linalg.solve(matLU,matBx) # solve matricies
                coeffs = []
                for i in range(0, x + 1): # strip coefficeints out
                    coeffs.append(done.item(i))
                coeffs.reverse()
                lastpoly = poly
                lasteval = eval
                poly = Polynomial(coeffs) # create polynomial 
                eval = poly.evaluate(self.data[indepIndex]) # get fi
                sfi = 0
                for i in range(0, self.lenData): # get sum of residuals
                    val = yval[i] - eval[i]
                    val *= val
                    sfi += val
                lastrsq = rSquared
                rSquared = 1 - (sfi / syi) # rsquared value
                lastdiff = diff
                diff = 1-(lastrsq/ rSquared)
                if diff == 0:
                    diff = 1e-16
                polyArr.append((poly,rSquared,lastdiff/diff))
                if (lastrsq > rSquared):
                    break
                currArr = np.multiply(currArr,self.data[indepIndex]) # add next order data
                AT.append(currArr) # append to AT 2D matrix
            maxvalue = 0
            maxpoly = None
            maxindex = 0
            for i in range(0,len(polyArr)): # find lowest lastdiff / diff value
                if polyArr[i][2] > maxvalue:
                    maxvalue = polyArr[i][2]
                    maxindex = i
            return polyArr[maxindex][0], polyArr[maxindex][1]

        else: # definite degree solution
            for x in range(1,degree):
                currArr = np.multiply(currArr,self.data[indepIndex]) # add next order data
                AT.append(currArr) # append to AT 2D matrix
            matAT = np.matrix(AT) # get Atranspose
            matA = matAT.transpose()
            matLU = matAT * matA # Atranspose * A
            matBx = matAT * matB # Atranspose * B
            done = np.linalg.solve(matLU,matBx) # solve matricies
            coeffs = []
            for i in range(0, degree + 1): # strip coefficeints out
                coeffs.append(done.item(i))
            coeffs.reverse()
            poly = Polynomial(coeffs) # create polynomial
            eval = poly.evaluate(self.data[indepIndex]) # get fi
            sfi = 0
            for i in range(0, self.lenData): # get sum of residuals
                val = yval[i] - eval[i]
                val *= val
                sfi += val
            rSquared = 1 - (sfi / syi) # rsquared value
            return poly, rSquared



    def __str__(self):
        """string representation of dataset"""
        dataStr = ""
        for x in range (0, self.numVars):
            dataStr += str(self.dataNames[x])
            dataStr += ":\t\t"
        dataStr += "\n"
        if self.lenData > 0:
            for y in range (0, self.lenData):
                for x in range (0, self.numVars):
                    dataStr += str(self.data[x][y])
                    dataStr += "\t\t"
                dataStr += "\n"
        return dataStr

    def getStats(self, varName):
        """returns mean and standard deviation for a specific variable"""
        index = self.dataNames.index(varName) # get variable index
        return np.mean(self.data[index]), np.std(self.data[index]) # get mean and stddev

    def getMinMax(self, varName):
        """returns min and max values for a specific variable"""
        index = self.dataNames.index(varName) # get variable index
        if self.lenData > 0:
            minval = self.data[index][0]
            maxval = self.data[index][0]
            for x in range(1,self.lenData): # get max min
                newval = self.data[index][x]
                if newval < minval: # check if new min
                    minval = newval
                elif newval > maxval: # check if new max
                    maxval = newval
            return minval, maxval

    def getKmeans(self, varName, number = 2, maxIters = 1000):
        """gets a number of kmeans (default is 2) for a specific variable"""
        if number < 2:
            raise ValueError("can't have less than 2 kmeans")
        minval, maxval = self.getMinMax(varName) # get min max
        mean, stddev = self.getStats(varName) # get mean and stddev
        kmeans = [minval]
        if number > 2: # generate initial kmeans
            newKmean = minval   
            scale = (maxval - minval) / (number - 1)
            for x in range(1, number - 1):
                newKmean += scale
                kmeans.append(newKmean)
        kmeans.append(maxval)
        # iterate until complete
        dataArr = self.data[self.dataNames.index(varName)] # get data to use
        for x in range(0, maxIters):
            sortedValues = []
            for i in range(0, number):
                sortedValues.append([]) # create empty sorted array
            for values in dataArr: # sort elements
                sortIndex = 0
                minDist = abs(values - kmeans[sortIndex])
                for i in range(1, number): # check all kemans
                    newDist = abs(values - kmeans[i])
                    if newDist <= minDist: # check if shorter distance to kmean
                        sortIndex = i
                        minDist = newDist
                sortedValues[sortIndex].append(values) # append value to correct place
            # create new kmeans
            newKmeans = [] 
            for i in range(0, number):
                newKmean = 0
                for values in sortedValues[i]: # sum values near kmean
                    newKmean += values
                length = len(sortedValues[i])
                if  length > 0:
                    newKmeans.append(newKmean / length) # append new kmean
                else:
                    number -= 1
            # check for change in kmeans
            changed = False
            if len(kmeans) == len(newKmeans): # check if a kmean dissapeared
                for i in range(0, number):
                    if kmeans[i] != newKmeans[i]: # check for individual change
                        changed = True
                        break
                if changed == False: # check if no change occorred
                    break
            kmeans = newKmeans # update kmeans
        # finalization
        finalKmeans = []
        for i in range(0,number):
            finalKmeans.append((kmeans[i],np.std(sortedValues[i]))) # tuple (kmean, stddev of kmean)
        return finalKmeans

    def getMovAvg(self, varName, points, reverse = False):
        """gets moving average of variable of a number of points starting at back of dataset.
        can be reversed to use front of dataset"""
        index = self.dataNames.index(varName)
        if points > self.lenData:
            raise ValueError("Dataset doesn't have enough points")
        average = 0
        if reverse: # start at front of list
            for x in range(0,points):
                average += self.data[index][x] # increment sum
        else: # start at back of list
            for x in range((self.lenData - 1),((self.lenData - points) - 1), -1):
                average += self.data[index][x] # increment sum
        average /= points # divide by number of points
        return average