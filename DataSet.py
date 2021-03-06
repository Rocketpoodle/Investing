import numpy as np
import matplotlib.pyplot as plt
from Polynomial import *
import math
import random

class DataSet(object):
    """Data set is an object that holds datasets
       data must be of equal length"""
    
    dataNames = [] # holds string data names for data members
    data = [] # array of data arrays. Primary array index corresponds to data name index
    numVars = 0 # number of data variables (data sub arrays)
    lenData = 0 # length of data sub arrays
    varScale = [] # scale for variables
    varOffset = [] # offset for variables

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
        self.varScale = [1]*self.numVars
        self.varOffset = [0]*self.numVars

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

    def addDataVariable(self, varName, varData, scale = [0,1]):
        """adds variable to dataset (requires data of length equal to current data length)"""
        if self.dataNames.count(varName) != 0: # check if variable already exists
            raise ValueError("A variable of that name already exists")
        if self.lenData != len(varData): # check that data is same length
            raise ValueError("New data is not of the correct length")
        self.data.append(varData) # append variable
        self.dataNames.append(varName)
        self.varOffset.append(scale[0])
        self.varScale.append(scale[1])
        self.numVars += 1 # increment number of variables

    def delDataVariable(self, varName):
        """removes variable from dataset"""
        if self.dataNames.count(varName) == 0: # check if variable already exists
            raise ValueError("Variable not found")
        self.numVars -= 1 # decrement variable
        popindex = self.dataNames.index(varName)
        self.dataNames.pop(popindex)
        self.varOffset.pop(popindex)
        self.varScale.pop(popindex)
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

    def getDataVariable(self, varName, scaled = True):
        """gets data array for varname"""
        index = self.dataNames.index(varName)
        if scaled == False: # if data needs to be descaled
            return [(x - self.varOffset[index])*self.varScale[index] for x in self.data[index]]
        return self.data[index].copy()

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
    
    def descaleDataVariable(self, varName):
        """reverses scaling on data variables"""
        index = self.dataNames.index(varName)
        if self.lenData == 0: # check for empty data or 0 scale
            return None
        for x in range(0,self.lenData): # scale values
            newval = (self.data[index][x] - self.varOffset[index])*self.varScale[index]
            self.data[index][x] = newval
        self.varScale[index] = 1
        self.varOffset[index] = 0
        return index

    def scaleDataVariable(self, varName, start = -1, end = 1):
        """scales vales to range from start to end"""
        self.descaleDataVariable(varName) # first remove any current scaling
        index = self.dataNames.index(varName)
        if self.lenData == 0 or (end - start) == 0: # check for empty data or 0 scale
            return None
        minval, maxval = self.getMinMax(varName)
        scale = (maxval - minval) / (end - start)
        start -= (minval / scale)
        for x in range(0,self.lenData): # scale values
            newval = (self.data[index][x] / scale) + start
            self.data[index][x] = newval
        self.varScale[index] *= scale
        self.varOffset[index] += start
        return scale, start

    def getVarScale(self, varName):
        """gets variable scaling information"""
        index = self.dataNames.index(varName) # get var index
        return [self.varOffset[index], self.varScale[index]]

    def plotData(self, independant, dependant, scaled = True, blocking = True, scatter = None):
        """plots data of dataset, specifying name of independant variable and dependant variable(s).
        can specify plot arguments"""
        if scatter == None or len(scatter) != len(dependant): # setup scatter array
            scatter = []
            for names in dependant:
                scatter.append(False)
        xVals = self.getDataVariable(independant,scaled)
        for i in range(0, len(dependant)): # plot data according to specification
            if scatter[i]:
                plt.scatter(xVals,self.getDataVariable(dependant[i],scaled))
            else:
                plt.plot(xVals,self.getDataVariable(dependant[i],scaled))
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
        if syi == 0:
            syi = 2e-17
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
            degree = self.lenData
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
                if coeffs[0] != 0:
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
                        diff = 2e-17
                    if (lastrsq > rSquared):
                        break
                    polyArr.append((poly,rSquared,diff/lastdiff))
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

    def getDistance(self, p1, p2):
        """returns Euclidean distance between two points at index i1 and i2"""
        sumofsquares = 0
        for x in range(0,self.numVars): # sum of squares
            diff = p1[x] - p2[x] # difference
            sumofsquares += diff*diff # add square of difference 
        if sumofsquares < 0:
            return cmath.sqrt(sumofsquares) # less than 0
        return math.sqrt(sumofsquares) # distance

    def getCurveFitEasy(self, independant, dependant):
        """gets curve fit using default settings and scales data to give best results
        then appends data as new variable with name fit_<dependant>"""
        self.scaleDataVariable(independant)
        newName = "fit_" + dependant
        fit, rsq = self.curveFit(independant, dependant)
        fitdata = fit.evaluate(self.getDataVariable(independant))
        xscaling = self.getVarScale(independant)
        fit.setScale(xscaling[1], xscaling[0])
        self.addDataVariable(newName , fitdata)
        self.descaleDataVariable(independant)
        return newName, fit, rsq

    def getDisttoKmean(self, index , point):
        """gets distance from point at index to point"""
        if self.numVars != len(point):
            raise ValueError("Data and point must have same variables")
        sumofsquares = 0
        for x in range(0,self.numVars): # sum of squares
            diff = self.data[x][index] - point[x] # difference expecting tuple (
            sumofsquares += diff*diff # add square of difference 
        if sumofsquares < 0:
            return cmath.sqrt(sumofsquares) # less than 0
        return math.sqrt(sumofsquares) # distance

    def kmeanAnalysis(self, sigmaScale = 2, startNum = 2, refineSigma = None, trimSig = None, refine = True, trim = False):
        """runs kmean analysis on dataset. Generates as many kmeans as necessary
        maxing at length of dataset/2. Returns kmean tuples (kmean, stddev, numValues).
        kmean is added when points fall within 2 (sigmaScale) sigma of each other"""
        # check refinement sigma scale
        if refineSigma == None:
            refineSigma = 1
        if trimSig == None:
            trimSig = 1
        if self.lenData < 2:
            raise ValueError("Need at least 2 datapoints")
        # initialize to 2 kmeans (kmeans can be on top of each other to start)
        kmeans = []
        # initialize starting kmeans
        for x in range(0, startNum):
            kmeans.append([self.getDataPoint(random.randrange(0, self.lenData)), 0, 0])
        # main loop
        numMeans = 0
        sil = 0
        bestSorted = None
        bestMeans = None
        while (numMeans < self.lenData):
            # initialize kmeans and values struct
            numMeans = len(kmeans)
            newKmeans = []
            sortedVals = []
            sortedDist = []
            for x in range(0,numMeans):
                sortedVals.append([]) # 2d array initialization
                sortedDist.append([])
            # sort values
            for i in range(0, self.lenData):
                lowIndex = 0
                lowDist = self.getDisttoKmean(i, kmeans[0][0]) # get first dist
                for j in range(1, numMeans):
                    dist = self.getDisttoKmean(i, kmeans[j][0]) # get curr dist
                    if dist < lowDist:
                        lowIndex = j
                        lowDist = dist
                sortedVals[lowIndex].append(self.getDataPoint(i)) # append to correct sort location
                sortedDist[lowIndex].append(lowDist) # append distance
            # update kmeans
            for i in range(0, numMeans):
                K = [[],0,0] # new kmean array
                striplen = len(sortedVals[i])
                if striplen > 0: # check if kmean got any values
                    for h in range(0, self.numVars):
                        strippedArr = []
                        mean = 0
                        for j in range(0, striplen): # strip array from 2d array
                            val = sortedVals[i][j][h]
                            strippedArr.append(val)
                            mean += val
                        mean /= striplen
                        newSigma = np.mean(sortedDist[i])
                        K[0].append(mean) # get kmean 
                        K[1] = newSigma
                        K[2] = striplen
                else: # if kmean got no values re-initialize
                    K = [self.getDataPoint(random.randrange(0, self.lenData)), 0, 0]
                newKmeans.append(K) # append new Kmean
            # determine if changes were made
            same = (kmeans == newKmeans)
            if same: # done if no change has occured
                # determine score of Kmean
                lastSil = sil
                sil = self.getSilCoeff(newKmeans)
                if sil > lastSil:
                    bestMeans = newKmeans.copy()
                    bestSorted = sortedVals.copy()
                # break if done
                else:
                    break
                # find kmean with most variance and add kmean to that set
                maxVar = 0
                maxIndex = 0
                for x in range(0, numMeans):
                    if newKmeans[x][1] > maxVar:
                        maxVar = newKmeans[x][1]
                        maxIndex = x
                randPoint = sortedVals[maxIndex][random.randrange(0, len(sortedVals[maxIndex]))] # get random point
                newK = []
                for i in range(0, self.numVars):
                    newK.append((randPoint[i] + newKmeans[maxIndex][0][i]) /2) # average kmean and point to get new kmean
                newKmeans.append([newK , 0, 0])
            # update kmeans structure
            kmeans = newKmeans
        # return final Kmeans
        kmeans = bestMeans
        sortedVals = bestSorted
        # mean refinement
        if refine:
            # intialize values
            numMeans = len(kmeans)
            newSorted = []
            newDist = []
            newKmeans = []
            for x in range(0,numMeans):
                newSorted.append([]) # 2d array initialization
                newDist.append([])
            # step through all means removing any points outside refinement range
            for x in range(0, numMeans):
                for values in sortedVals[x]:
                    dist = self.getDistance(kmeans[x][0], values)
                    # check if within sigma range
                    if dist <= refineSigma*kmeans[x][1]:
                        newSorted[x].append(values)
                        newDist[x].append(dist)
            # update means
            for i in range(0, numMeans):
                K = [[],0,0] # new kmean array
                striplen = len(newSorted[i])
                if striplen > 0: # check if kmean got any values
                    for h in range(0, self.numVars):
                        strippedArr = []
                        mean = 0
                        for j in range(0, striplen): # strip array from 2d array
                            val = newSorted[i][j][h]
                            strippedArr.append(val)
                            mean += val
                        mean /= striplen
                        newSigma = np.std(newDist[i])
                        K[0].append(mean) # get kmean 
                        K[1] = newSigma
                        K[2] = striplen
                    newKmeans.append(K) 
            kmeans = newKmeans
            sortedVals = newSorted
        # mean Trimming
        if trim:
            newKmeans = []
            sigArr = []
            numArr = []
            numMeans = len(kmeans)
            # get array of kmean sigmas
            for x in range(0, numMeans):
                sigArr.append(kmeans[x][1] / kmeans[x][2])
                numArr.append(kmeans[x][2])
            # get std of kmean sigmas
            sigstd = np.std(sigArr)
            meanSig = np.mean(sigArr)
            print("Trim above:", meanSig + trimSig*sigstd)
            # remove kmeans that are outside of the sigma range
            numPop = 0
            for x in range(0, numMeans):
                if (kmeans[x][1] / kmeans[x][2]) <= meanSig + trimSig*sigstd: 
                    newKmeans.append(kmeans[x])
                else:
                    sortedVals.pop(x - numPop)
                    numPop += 1
            kmeans = newKmeans
        # evaluate output means
        if len(kmeans) > 1:
            DI = self.getDunnIndex(kmeans)
            DB = self.getDaviesBouldin(kmeans)
            sil = self.getSilCoeff(kmeans)
        else:
            DI = 0
            DB = 0
            sil = 0
        return (kmeans, sil, DI, DB)

    def getDaviesBouldin(self, kmeans):
        """ Gets Davies-Bouldin index for Kmeans.
        Sum of the maximum for each mean for the two sigmas over the distance between centroids"""
        # initialize values
        DB = 0
        numMeans = len(kmeans)
        # step through all points
        for i in range(0, numMeans):
            for j in range(0, numMeans): # calculate for all other points
                maxValue = 0
                if not i == j: # skip self
                    # calculate distance
                    dist = self.getDistance(kmeans[i][0], kmeans[j][0])
                    value = (kmeans[i][1] + kmeans[j][1]) / dist # divide sum of sigmas by distance
                    # check if new maximum
                    if value > maxValue:
                        maxValue = value
            DB += maxValue # add maximum to index value
        DB /= numMeans # divide by number of means to get final value
        return DB

    def getDunnIndex(self, kmeans):
        """ Gets Dunn index for Kmeans.
        minimum distance between clusters over maximum cluster sigma"""
        numMeans = len(kmeans)
        maxVal = kmeans[numMeans-1][1] # initialize to last sigmas since it wont be checked later
        minVal = None
        # calculate min and max values
        for i in range(0, numMeans-1):
            for j in range(i+1, numMeans): # calculate for all other points (except self)
                dist = self.getDistance(kmeans[i][0], kmeans[j][0])
                # update minval
                if minVal == None:
                    minVal = dist
                elif dist < minVal:
                    minVal = dist
            # update maxVal
            if kmeans[i][1] > maxVal:
                maxVal = kmeans[i][1]
        DI = minVal / maxVal
        return DI

    def getSilCoeff(self, kmeans):
        """silhouette coefficient contrasts average distance other points"""
        # initialize
        numMeans = len(kmeans)
        silCoeff = 0
        # step through all means
        for i in range(0, numMeans):
            Ai = kmeans[i][1]
            Bi = None
            for j in range(0, numMeans):
                # if i == j then update intra cluster distance
                if i != j:
                    dist = self.getDistance(kmeans[i][0], kmeans[j][0])
                    if Bi == None:
                        Bi = dist
                    elif dist < Bi:
                        Bi = dist
            # get max of A(i) and B(i)
            silCo = Bi - Ai
            if Bi < Ai:
                silCo /= Ai
            else:
                silCo /= Bi
                silCo *= kmeans[i][2]
                silCoeff += silCo # append silhouette coefficient
        silCoeff /= self.lenData
        return silCoeff
