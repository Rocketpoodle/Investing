import csv
import matplotlib.pyplot as plt
import numpy as np
import random
import fetchSqlData
import initDB
import time
import math
from matplotlib.figure import Figure

def getPointSet(symbol,size):
    """
    getPointSet: generates points list from csv file
    file - String filename to read must be csv format
    size - Int size of range to select 0 returns all points
    return: list of points from csv file
    """
    DB = initDB.dbLogin()
    start = time.time()
    pointset = fetchSqlData.getPoints(symbol, ["Date, AdjClose"], DB)
    end = time.time()
    #print(end - start)
    # create range randomly if size is not 0
    if size > 0:
        r1 = random.randint(0,len(pointset) - 1)
        r2 = r1 + size
        pointset = pointset[r1:r2]
    return pointset

def evalPoly(constArr, x):
    """
    evalPoly: evaluates polynomial described by constArr at value x
    constArr - array of constants for the polynomial where lowest index is lowest order
    x - value to evaluate at
    return: the polynomial functions value y(x)
    """
    i = 0
    y = 0
    while i < len(constArr):
        y += float(constArr[i] * pow(x, i))
        i += 1
    return y

def derivPoly(constArr):
    """
    derivPoly: finds derivative of polynomial described by constArr
    constArr - array of constants for the polynomial where lowest index is lowest order
    return: the derivative of the polynomial as new array of constants
    """
    deriv = []
    for i in range(1,len(constArr)):
        newConst = constArr[i]*i
        deriv.append(newConst)
    return deriv

def polyFit(pointset,order):
    """
    polyFit: creates polynomial fit of degree order for set of points pointset
    pointset - set of points to find curve fit
    order - degree of polynomial to use
    return: polynomial curve fit as constant array, r squared value, and weighted r squared value
    method: solve as systems of equaitons for sum of squares minimization
    """
    # create matrix A as equation terms (left side)
    matA = []
    for r in range(order, -1, -1):
        rowsA = []
        for c in range(order, -1, -1):
            value = 0
            i = 0
            while i < len(pointset):
                value += pow(i,r + c)
                i += 1
            rowsA.append(float(value))
        matA.append(rowsA)
    # create matrix B as equation constant (right side)
    matB = []
    for r in range(order, -1, -1):
        rowB = []
        value = 0
        i = len(pointset) - 1
        j = 0
        while i >= 0:
            value += (float(pointset[j][1])*pow(j,r))
            i -= 1
            j += 1
        rowB.append(value)
        matB.append(rowB)
    # invert matrix A then multiply by matrix B
    matA = np.matrix(matA)
    matB = np.matrix(matB)
    imatA = np.linalg.inv(matA)
    matX = imatA*matB
    fitSet = []
    for var in range(order, -1, -1):
        fitSet.append(float(matX[var][0]))
    # determine r squared value for reference
    i = len(pointset) - 1
    j = 0
    newrs = 0
    average = 0
    while i > 0:
        average += float(pointset[j][1])
        newrs += (pow(float(pointset[j][1]) - evalPoly(fitSet,j),2))
        i -= 1
        j += 1
    wrs = newrs / (average / len(pointset))
    return [fitSet,newrs,wrs]

def drawPoints(pointset,polyset):
    """
    drawPoints: draws the points in pointset with the polynomial fit polyset using matplotlib
    pointset - set of points to draw
    polyset - constant array for polynomial fit
    return: None
    """
    i = len(pointset) - 1
    j = 0
    a = []
    b = []
    c = []
    # generates plot sets using pointset and index
    while i >= 0:
        a.append(j)
        b.append(float(pointset[j][1]))
        c.append(evalPoly(polyset,j))
        i -= 1
        j += 1
    plt.plot(a,b)
    plt.plot(a,c)
    plt.show()

def getmean(pointset):
    """
    getMean: finds the mean of the points pointset
    pointset - set of points to find the mean of
    return: float value of mean
    """
    total = 0
    range = len(pointset)
    for points in pointset:
        total += float(points[1])
    mean = total/range
    return mean

def getKmean(pointset):
    """
    getKmean: finds 2 means using k-means algorithm
    pointset - set of points to find k-means of
    return: meanh,meanl the high and low k-means respectively
    """
    high = float(pointset[0][1])
    low = float(pointset[0][1])
    # starts by arbitrarily setting high and low means to highest and lowest value
    for points in pointset:
        if float(points[1]) < low:
            low = float(points[1])
        if float(points[1]) > high:
            high = float(points[1])
    meanh = high
    meanl = low
    done = False
    # k-mean algorithm loop
    while not done:
        highlist = []
        lowlist = []
        # divide points into high and low set
        for points in pointset:
            value = float(points[1])
            dlow = abs(value - meanh)
            dhi = abs(meanl - value)
            if dhi > dlow:
                highlist.append(points)
            elif dlow > dhi:
                lowlist.append(points)
        # calculate new means
        meanh2 = getmean(highlist)
        meanl2 = getmean(lowlist)
        # if means dont change then finish
        if meanh2 == meanh and meanl2 == meanl:
            done = True
        meanh = meanh2
        meanl = meanl2
        
    return [meanh,meanl]

def getProfit(pointset,khi,klow):
    """
    getProfit: gets profit over pointset using arbitrary buy/sell points klow and khi
    pointset - set of points to find profit on
    khi - arbitrary sell price
    klow - arbitrary buy price
    return: profit,percet,crossing - total profit, profit as percent of input, number of changes between low and high
    """
    maxi = len(pointset) - 1
    profit = 0
    inVal = 0
    i = maxi
    crossing = 1
    # step through points to see if its worth buying
    while i >= 0:
        value = float(pointset[i][1])
        if value < klow:
            # buy and then step to find sell point
            inVal += value
            crossing += 1
            for j in range(i,-1,-1):
                newVal = float(pointset[j][1])
                # sell at sell pint or end of range
                if newVal > khi or j == 0:
                    crossing += 1
                    # add profit and change j to current position
                    profit += (newVal - value)
                    i = j
                    break
        i -= 1
    percent = (profit/inVal)*100    
    return [profit,percent,crossing]

def getScore(pointset, fit, kmeans):
    # TODO: add commenting and make effecient
    #deltaK = kmeans[0] - kmeans[1]
    kbuy = (kmeans[1] - pointset[len(pointset) - 1][1]) / kmeans[1]
    if kbuy < 0:
        kbuy = 1 / (abs(kbuy) + 2)
    else:
        kbuy += 1
    mean = getmean(pointset)
    #deltaK = deltaK / mean
    #wrs = fit[2]
    #fitDeriv = derivPoly(fit[0])
    #fitDeriv2 = derivPoly(fitDeriv)
    size = len(pointset)
    #slope = (evalPoly(fitDeriv, size) + evalPoly(fitDeriv, size - 1) + evalPoly(fitDeriv, size - 2)) / 3
    #trueS = pointset[size - 1][1] - pointset[size - 2][1]
    #slope = (slope + trueS)*(slope - trueS) / 2
    minArr = []
    maxArr = []
    minArr.append(evalPoly(fit[0],0))
    minArr.append(evalPoly(fit[0],size - 1))
    maxArr.append(evalPoly(fit[0],0))
    maxArr.append(evalPoly(fit[0], size - 1))
    for x in range(2,len(pointset)):
        i1 = evalPoly(fit[0], (x-2))
        i2 = evalPoly(fit[0], (x-1))
        i3 = evalPoly(fit[0], x)
        if i2 > i3 and i2 > i1:
            maxArr.append(i2)
        elif i2 < i3 and i2 < i1:
            minArr.append(i2)
        if pointset[x - 1][1] * 4 < pointset[x - 2][1]:
            return [0]
    maxr = max(maxArr) - min(maxArr)
    minr = max(minArr) - min(minArr)
    numM = len(minArr) + len(maxArr)
    sumr = (mean * numM) / (minr + maxr)
    score = sumr * kbuy * math.sqrt(mean)
    return score#,deltaK,slope,numM,sumr,kbuy]

def appendHigher(value, array, size):
    """
    appendHigher: inserts value into array if it is large enough
    value - value to insert
    array - array to insert into
    size - max size of array
    return: no return, instead array is modified to have the new value in its corresponding position
    """
    # if array is empty append the value
    if not array:
        array.append(value)
    # otherwise check where to append value
    else:
        for x in range(0,len(array) + 1):
            # check each element to see if value is higher
            try:
                if value > array[x]:
                    # insert if it is higher
                    array.insert(x, value)
                    break
            # if index is above length of array
            except:
                array.append(value)
        # get rid of all values past desired size
        while len(array) > size:
            array.pop()
"""
stockPoints = getPointSet("AAPL", 252)
score = 0
bestscores = []
best = stockPoints
for runs in range (0,100):
    try:
        stockPoints = getPointSet("AAPL", 252)
        secondary = stockPoints[192:252]
        kmeans2 = getKmean(secondary)
        fit2 = polyFit(secondary, 9)
        kmeans = getKmean(stockPoints)
        fit = polyFit(stockPoints, 9)
        newscore = 4*(getScore(stockPoints, fit, kmeans)[0]) + (getScore(secondary, fit2, kmeans2)[0])
        if newscore > score:
            score = newscore
            bestscores = getScore(stockPoints, fit, kmeans)
            best = stockPoints
    except:
        pass
print(bestscores)
fit = polyFit(best, 9)
drawPoints(best,fit[0])
"""
"""
DB = initDB.dbLogin()
stocksSet = fetchSqlData.getStockList(DB)
startIndex = 0
endIndex = 252
score = 0
best = 0
bestscores = 0
name = ""
number = 0
for stocks in stocksSet:
    number += 1
    symbol = stocks[0]
    print(number, symbol)
    stockPoints = fetchSqlData.getPoints(symbol, ["Date, AdjClose"], DB)
    stockPoints = stockPoints[0:252]
    try:
        secondary = stockPoints[-60:]
        kmeans2 = getKmean(secondary)
        fit2 = polyFit(secondary, 9)
        kmeans = getKmean(stockPoints)
        fit = polyFit(stockPoints, 9)
        newscore = 4 * (getScore(stockPoints, fit, kmeans)[0]) + (getScore(secondary, fit2, kmeans2)[0])
        if newscore > score:
            score = newscore
            bestscores = getScore(stockPoints, fit, kmeans)
            best = stockPoints
            name = symbol
    except:
        pass

print(bestscores)
fit = polyFit(best, 9)
drawPoints(best, fit[0])
"""
