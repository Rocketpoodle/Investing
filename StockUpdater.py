__author__ = 'Austin'

import csv
import re
import urllib.request


def updateAllStocks():
    updateOccurred = True
    fileNum = 1
    urlFull = "http://download.finance.yahoo.com/d/quotes.csv?s=%40%5EDJI"
    urlTail = "&f=sd1ohgl1v"
    k = 0
    #get last ticker
    stockListFile = open("GoodStocks.csv", 'r', newline='')
    goodListCsv = csv.reader(stockListFile)
    lastTicker = ""
    for row1 in goodListCsv:
        lastTicker = row1[0]
    currTicker = ""
    #iterate through all stocks
    stockListFile = open("GoodStocks.csv", 'r', newline='')
    goodListCsv = csv.reader(stockListFile)
    for row2 in goodListCsv:
        #update url
        if not row2[0] == "/START/":
            currTicker = row2[0]
            urlFull += ","
            urlFull += currTicker
            k += 1
        #only get file when 200 tickers are present or all tickers accounted for
        if k == 200 or currTicker == lastTicker:
            print(fileNum)
            fileNum += 1
            #add tail to url
            urlFull += urlTail
            #create set of 200 stocks in quotes file to update with
            urllib.request.urlretrieve(urlFull, "./newdata/quotes.csv")
            file = open("./newdata/quotes.csv", 'r', newline='')
            newData = csv.reader(file)
            for row in newData:
            #   create new row to append
                newRow = [row[1],row[2],row[3],row[4],row[5],row[6],row[5]]
            #   get current file contents
                with open("./data/"+row[0]+".csv", 'r', newline='') as oldData:
                    oldCsv = csv.reader(oldData)
                    rowArray = []
                    for rows in oldCsv:
                        rowArray.append(rows)
                oldData.close()
            #   update file data
                with open("./data/"+row[0]+".csv", 'w', newline='') as updated:
                    updatedCsv = csv.writer(updated)
                    updatedCsv.writerow(rowArray[0])
                    if(re.sub('[/-]','',rowArray[1][0]) != re.sub('[/-]','',newRow[0])):
                        updatedCsv.writerow(newRow)
                    else:
                        updateOccurred = False
                    i = 1
                    while i < len(rowArray):
                        updatedCsv.writerow(rowArray[i])
                        i += 1
                updated.close()
            k = 0
            urlFull = "http://download.finance.yahoo.com/d/quotes.csv?s=%40%5EDJI"
    return updateOccurred