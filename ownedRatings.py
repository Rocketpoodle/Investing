import csv

def getOwnedRatings():
    owned = []
    with open("./ratings/currRatings.csv", 'r', newline='') as ratedFile:
        ratedReader = csv.reader(ratedFile)
        for ratedRows in ratedReader:
            currTicker = ratedRows[0]
            stockOwned = False
            with open("./broker/ownedStocks.csv", 'r', newline='') as ownedFile:
                ownedReader = csv.reader(ownedFile)
    # check if the stock is owned or not
                for ownedRows in ownedReader:
                    if ownedRows[0] == ratedRows[0]:
                        stockOwned = True
    # only worries about stock if it is owned
            if stockOwned:
                currRating = float(ratedRows[1])
    # handle empty array
                if len(owned) == 0:
                    owned.append(ratedRows)
                else:
    # step through top 10
                    i = 0
                    added = False
                    for elements in owned:
                        testValue = float(elements[1])
                        if testValue > currRating:
                            owned.insert(i, ratedRows)
                            added = True
                            break
                        i += 1
                    if (not added):
                        owned.append(ratedRows)
    # print ratings
    print("\n--- Owned ---\n")
    for ratedStocks in owned:
        printString = ratedStocks[0] + ": "
        printString += ratedStocks[1]
        print(printString)