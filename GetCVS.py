import urllib.request
import bs4
import csv
import time


def fetchAllStocks():
    finalTicker = "AVAV"
    running = True
    while running:
        stockAt = -2
        startTime = time.time()
        lastStock = ""
        newStock = False
        stocksRead = 0
        #check for last stock ticker
        with open("GoodStocks.csv", 'r', newline='') as goodStocks:
            goodList = csv.reader(goodStocks)
            for row in goodList:
                lastStock = row[0]
        #loop through stocks recording stocks that have info
        with open("GoodStocks.csv", 'a', newline='') as goodStocks:
            goodList = csv.writer(goodStocks)
            with open("ValidTickers.csv", 'r', newline='') as stockFile:
                stockList = csv.reader(stockFile)
                for row in stockList:
                    stockAt += 1
                    #only read 10 then save files
                    if not row[0] == "/START/":
                        if stocksRead > 10:
                            print(stockAt)
                            break
                        ticker = row[0].strip()
                        #if new stock get file
                        if lastStock == "/START/":
                            newStock = True
                        if newStock:
                            print(str(stocksRead) + " " + ticker)
                            stocksRead += 1
                            try:
                                urllib.request.urlretrieve("http://finance.yahoo.com/q/hp?s=" + ticker + "+Historical+Prices","TEMP.html")
                            except urllib.error.HTTPError:
                                print('**BAD**')
                            with open("TEMP.html", 'r') as stock:
                                stockSoup = bs4.BeautifulSoup(stock)
                                #handle no donwload errors
                                try:
                                    stockLink = stockSoup.find_all('p')[1].find_all('a')[0].get('href')
                                    #handle cant reach download error
                                    try:
                                        urllib.request.urlretrieve(stockLink, "./data/" + ticker + ".csv")
                                        goodList.writerow([ticker])
                                    except urllib.request.http.client.IncompleteRead:
                                        print('**BAD**')
                                    except FileNotFoundError:
                                        print('**BAD**')
                                except IndexError:
                                    print('**BAD**')
                        #enable saving information
                        if ticker == lastStock:
                            newStock = True
                        #stop program when final ticker is reached
                        if ticker == finalTicker:
                            running = False
        stopTime = time.time()
        print(("%.2f" % (stopTime - startTime)) + " s")