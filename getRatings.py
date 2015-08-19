import csv
import math


def getAllRatings():
    with open("ValidTickers.csv", 'r', newline='') as tickerFile:
        with open("./ratings/currRatings.csv", 'w', newline='') as ratingsFile:
            tickerReader = csv.reader(tickerFile)
            ratingsWriter = csv.writer(ratingsFile)
            tickerReader.__next__()
    # step through all stocks
            print("\nError with file(s): \n")
            for row in tickerReader:
                try:
                    with open("./data/"+row[0]+".csv", 'r', newline='') as stockFile:
                        stockReader = csv.reader(stockFile)
                        stockReader.__next__()
    # define arrays for holding moving average and trend points
                        trend = 0
                        movAvg = 0
                        rating = 0
                        previousClose = 0
                        noData = False
                        currClose = 0
                        movAvg5 = 0
                        movAvg5day2 = 0
                        finalPreviousClose = 0
    # loop through 60 days (market days)
                        i = 1
                        while i <= 60:
                            try:
                                point = stockReader.__next__()
                            except StopIteration:
                                noData = True
                                break
    # stops loop if not 60 days of data
                            if point == None:
                                noData = True
                                break
                            try:
                                close = float(point[4])
                            except ValueError:
                                noData = True
                                print(row[0])
                                break
                            except IndexError:
                                noData = True
                                print(row[0])
                                break
                            if i == 1:
                                currClose = close
                            if i == 2:
                                trend = previousClose - close
                                finalPreviousClose = close
                            if i <= 5:
                                movAvg5 += close
                            if i <= 6 and i > 1:
                                movAvg5day2 += close
                            movAvg += close
                            previousClose = close
                            i += 1
    # gets rating from calculated values
                        if not noData:
                            movAvg /= 60
                            movAvg5 /= 5
                            movAvg5day2 /= 5
                            rating += (trend / currClose)
                            subRating = ((movAvg - currClose)/movAvg)
                            rating *= subRating
                            rating *= math.sqrt(currClose)
                            rating *= 1000
                            if trend > 0  and subRating < 0:
                                rating *= 0.5
                            if trend < 0 and subRating < 0:
                                rating *= -1
                            if currClose >= movAvg5 and finalPreviousClose <= movAvg5day2:
                                rating *= 1.5
    # devalues stock if not enough data
                        else:
                            rating = -1000
    # write stock ticker with rating to file
                        ratingString = ("%.2f" % rating)
                        newRow = [row[0],ratingString]
                        ratingsWriter.writerow(newRow)
                except FileNotFoundError:
                    noData = True
                    print(row[0])
    # get top 10 ratings
    top10 = []
    with open("./ratings/currRatings.csv", 'r', newline='') as ratedFile:
        ratedReader = csv.reader(ratedFile)
        for ratedRows in ratedReader:
            currRating = float(ratedRows[1])
    # handle empty array
            if len(top10) == 0:
                top10.append(ratedRows)
            else:
    # step through top 10
                i = 0
                added = False
                for elements in top10:
                    testValue = float(elements[1])
                    if testValue < currRating:
                        top10.insert(i, ratedRows)
                        if len(top10) == 11:
                            top10.pop(10)
                        added = True
                        break
                    i += 1
                if (not added) and i < 10:
                    top10.append(ratedRows)
    # print top 10
    print("\n--- TOP 10 ---\n")
    for ratedStocks in top10:
        printString = ratedStocks[0] + ": "
        printString += ratedStocks[1]
        print(printString)

