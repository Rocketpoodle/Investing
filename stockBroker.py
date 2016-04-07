import csv
import GetCVS
import soloFetch
import getRatings
import StockUpdater
import ownedRatings
import fetchSqlData
from datetime import date,datetime,timedelta
import initDB

#================================================#
#===================== INIT =====================#
#================================================#

# Initialization occurs getting Bank money and stocks
BANK = 10000
DAY = 0
STOCKS = []
UNRESOLVED = 0
HOLDINGS = 0
CONNECTION = initDB.dbLogin()
BROKERNAME = "Broker1"
# gets bankroll and day
with open("./broker/brokerInfo.csv", 'r', newline='') as brokerFile:
    brokerReader = csv.reader(brokerFile)
    BANK = float(brokerReader.__next__()[0])
    DAY = int(brokerReader.__next__()[0])
# populates stock list from ownedStocks.csv
with open("./broker/ownedStocks.csv", 'r', newline='') as ownedStockFile:
    ownedStockReader = csv.reader(ownedStockFile)
    for ownedStockRow in ownedStockReader:
        newStockElement = [ownedStockRow[0],float(ownedStockRow[1]),int(ownedStockRow[2])]
        STOCKS.append(newStockElement)
    for stocksOwned in STOCKS:
        with open("./data/"+stocksOwned[0]+".csv", 'r', newline='') as ownedDataFile:
            ownedDataReader = csv.reader(ownedDataFile)
            ownedDataReader.__next__()
            currentPriceRow = ownedDataReader.__next__()
            currentPrice = float(currentPriceRow[4])
            currValue = currentPrice*float(stocksOwned[2])
            HOLDINGS += currValue
with open("./broker/unresolvedSale.csv", 'r', newline='') as unresolvedFile:
    unresolvedReader = csv.reader(unresolvedFile)
    for unresolvedRow in unresolvedReader:
        UNRESOLVED += float(unresolvedRow[1])

#================================================#
#============= FUNCTION DEFINITIONS =============#
#================================================#

def printOwnedStocks():
# printOwnedStocks pretty prints stocks owned
# prints ticker, buy price, and quantity
    i = 1
    for stockElements in STOCKS:
        print(str(i) + ". " + stockElements[0])
        print("Buy Price: " + ("%.2f" % stockElements[1]))
        print("Volume : " + str(stockElements[2]) + "\n")
        i += 1

def buyTransaction():
# buyTransaction handles a buy from transaction
# asks ticker, prints price, then prompts for quantity and validates against bankroll
# returns logstring to write to transactions.log
    global DAY
    global BANK
    global HOLDINGS
    try:
        buyTicker = input("Ticker to Buy: ")
        with open("./data/"+buyTicker+".csv", 'r', newline='') as buyStockFile:
            buyStockReader = csv.reader(buyStockFile)
            buyStockReader.__next__()
            buyStockRow = buyStockReader.__next__()
        priceOfStock = float(buyStockRow[4])
        print("Money in Bank: " + ("%.2f" % BANK))
        print("Share Price: " + ("%.2f" %priceOfStock))
        sharesToBuy = int(input("Quantity to Buy: "))
        priceToBuy = sharesToBuy*priceOfStock
        print("Purchase Price: " + ("%.2f" % (priceToBuy + 9)))
        # validate buy transaction
        validBuy = False
        if priceToBuy > BANK - 9:
            print("**Insufficient Funds**")
        else:
            confirmBuy = input("Confirm Buy (y/n): ")
            if confirmBuy == "y" or confirmBuy == "Y":
                validBuy = True
        # if buy is validated return string otherwise return none
        if validBuy:
            BANK -= (priceToBuy + 9)
            HOLDINGS += priceToBuy
            STOCKS.append([buyTicker,priceOfStock,sharesToBuy])
            returnString = "BUY "+buyTicker+" at "+("%.2f" % priceOfStock)+" "+str(sharesToBuy)+" shares\n"
            print("Bank: " + ("%.2f" % BANK))
            return returnString
        else:
            return None
    except FileNotFoundError:
        print("**NOT VALID TICKER**")
        return None

def sellTransaction():
# sellTransaction handles sell from transaction
# prints owned stocks, prompts for number corresponding to stock group
# prompts quantity to sell, decides whether to update existing stock or remove if all sold
# returns logString of sell
    global DAY
    global BANK
    global HOLDINGS
    printOwnedStocks()
    print("\n")
    sellTickerNum = int(input("Number of Ticker to Sell: "))
    sellStock = STOCKS[sellTickerNum - 1]
    sellTicker = sellStock[0]
    sellShares = int(sellStock[2])
    boughtPrice = float(sellStock[1])
    with open("./data/"+sellTicker+".csv", 'r', newline='') as sellStockFile:
        sellStockReader = csv.reader(sellStockFile)
        sellStockReader.__next__()
        sellStockRow = sellStockReader.__next__()
    valueOfStock = float(sellStockRow[4])
    print("\n" +sellTicker)
    print(str(sellShares) + " shares")
    print("Bought at: " +str(boughtPrice))
    print("Current value: " +str(valueOfStock))
    sharesToSell = int(input("\nNumber of Shares to Sell:"))
    totalSoldValue = sharesToSell*valueOfStock
    print("Sell "+ str(sharesToSell) + " for " + ("%.2f" % (totalSoldValue - 9)))
    # validate transaction
    validSell = False
    if sharesToSell > sellShares:
        print("**Insufficient Shares**")
    else:
        confirmSell = input("Sell Shares (y/n): ")
        if confirmSell == "y" or confirmSell == "Y":
            validSell = True
    # if its valid return log string otherwise do nothing
    if validSell:
        if sharesToSell == sellShares:
            STOCKS.pop(sellTickerNum - 1)
        else:
            sellStock[2] = sellShares - sharesToSell
        saleRow = [DAY + 3, totalSoldValue - 9]
        HOLDINGS -= totalSoldValue
        with open("./broker/unresolvedSale.csv", 'a', newline='') as salesFile:
            salesWriter = csv.writer(salesFile)
            salesWriter.writerow(saleRow)
        returnString = "SELL " + sellTicker + " at " + ("%.2f" % valueOfStock) + " " + str(sharesToSell) + " shares\n"
        return returnString
    else:
        return None

def transaction():
# transaction prompts if buy or sell and branches upon choice
# updates ownedStocks, transaction.log and brokerInfo upon end
    transactionReturn = None
    transactionType = input("buy or sell (b/s): ")
    if transactionType == "b" or transactionType == "B":
        transactionReturn = buyTransaction()
    elif transactionType == "s" or transactionType == "S":
        transactionReturn = sellTransaction()
    # make sure transaction took place
    if transactionReturn:
        with open("./broker/transactions.log", 'a', newline='') as transactionLog:
            transactionLog.write(transactionReturn)
        with open("./broker/ownedStocks.csv", 'w', newline='') as updateOwnedFile:
            updateOwnedWriter = csv.writer(updateOwnedFile)
            for updatedStocks in STOCKS:
                updateOwnedWriter.writerow(updatedStocks)
        with open("./broker/brokerInfo.csv", 'w', newline='') as brokerInfoFile:
            brokerInfoWriter = csv.writer(brokerInfoFile)
            brokerInfoWriter.writerow([BANK])
            brokerInfoWriter.writerow([DAY])

def updateStockData():
# updateStockData updates stocks and increments day if update occurs
# prints if sales were resolved
    didUpdate = StockUpdater.updateAllStocks()

def printLog():
# printLog prints all entries in log file
    transactionCost = 0
    with open("./broker/transactions.log", 'r', newline='') as printLogFile:
        for line in printLogFile:
            print(line)
            transactionCost += 9
    print("Broker Fees: " + str(transactionCost))

def incrementDay(broker):
    """
    incrementDay: increments day for broker
    broker - string broker name to increment day for
    return: True if day was incremented or False if end of range
    """
    # fetch current date
    currInfo = fetchSqlData.fetchBrokerInfo(broker,CONNECTION)
    date = currInfo[2]
    newDate = date + timedelta(days=1)
    today = datetime.today().date()
    # run until next trading day
    while not fetchSqlData.dateExists(newDate,CONNECTION):
        # done if day is >= today
        if newDate >= today:
            return False
        newDate = newDate + timedelta(days=1)
    # set new date for broker
    return fetchSqlData.setBrokerInfo(currInfo[0],currInfo[1],newDate,CONNECTION)

#================================================#
#===================== MAIN =====================#
#================================================#
print("\nDay: " + str(DAY))
print("Bank: " + ("%.2f" % BANK))
print("Pending Sales: " + ("%.2f" % UNRESOLVED))
print("Total Holdings Value: " + ("%.2f" % HOLDINGS))
while True:
    print("\nChoose Action:\n\n0. Re-print Broker Data\n1. Print Owned Stocks\n2. Rate Owned Stocks\n3. Rate All Stocks\n4. Make Transaction\n5. Update Data\n6. Re-fetch One Stock\n7. Re-fetch All Stocks\n8. Print Transaction Log\n9. Increment Day\nQ. EXIT\n")
    choice = input("")
    if choice == "Q" or choice == "q":
        break
    try:
        choice = int(choice)
        if choice == 1:
            printOwnedStocks()
        elif choice == 2:
            ownedRatings.getOwnedRatings()
        elif choice == 3:
            getRatings.getAllRatings()
        elif choice == 4:
            transaction()
        elif choice == 5:
            updateStockData()
        elif choice == 6:
            soloFetch.fetchOneStock(input("Ticker of Stock: "))
        elif choice == 7:
            GetCVS.fetchAllStocks()
        elif choice == 8:
            printLog()
        elif choice == 9:
            assurance = input("Are you sure (Y/n): ")
            if assurance == "Y" or assurance == "y":
                incrementDay()
        elif choice == 0:
            print("\nDay: " + str(DAY))
            print("Bank: " + ("%.2f" % BANK))
            print("Pending Sales: " + ("%.2f" % UNRESOLVED))
            print("Total Holdings Value: " + ("%.2f" % HOLDINGS))
    except ValueError:
        print("Invalid Input")