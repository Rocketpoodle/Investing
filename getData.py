import urllib.request
import json
import initDB
import csv
from datetime import date,datetime,timedelta
from os import remove
import psycopg2

def fetchStockInfo(connection):
    """
    fetchStockInfo: fetches stock ticker symbol, start date, and end date from yahoo and adds it to connection database
    connection - sql database connection
    return: string success or error info
    """
    stockNameSet = set()
    with open("STOCKLISTBIG.csv",'r') as stockList:
        stockListCsv = csv.reader(stockList,delimiter='|')
        for stockNames in stockListCsv:
            stockNameSet.add(stockNames[0])
    print(len(stockNameSet))
    # query for stocks in database
    sqlQuery = "SELECT Symbol FROM StockInfo;"
    DBcurr = connection.cursor()
    DBcurr.execute(sqlQuery)
    haveList = DBcurr.fetchall()
    DBcurr.close()
    connection.commit()
    # remove all duplicates from set
    for oldNames in haveList:
        try:
            stockNameSet.remove(oldNames[0])
        except KeyError:
            pass
    print(len(stockNameSet))
    # get info for each stock and add them to sql server
    n = 0
    t = 0
    tmax = len(stockNameSet)
    requestString = u"("
    errorString = ""
    for stocks in stockNameSet:
        requestString += "'" + stocks + "'"
        n += 1
        t += 1
        # check if request string is done
        if 100 or t == tmax:
            print(t)
            requestString += ")"
            # open cursor
            DBcurr = connection.cursor()
            # request json
            command = urllib.request.quote(u'select * from yahoo.finance.stocks where symbol in '+ requestString)
            fetch = urllib.request.urlopen("http://query.yahooapis.com/v1/public/yql?q=" + command +"&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=").read()
            fetch = json.loads(fetch.decode("utf-8"))["query"]["results"]["stock"]
            # go through items and submit to sql server
            sqlinsert = "INSERT INTO StockInfo (Symbol, Usable) VALUES"
            sqlitems = []
            onItem = 0
            # iterate through fetched items
            for items in fetch:
                try:
                    # insert comma when needed
                    if onItem > 0:
                        sqlinsert += ","
                    onItem += 1
                    # commit info to local sql server
                    sqlitems.append(items["symbol"])
                    sqlitems.append(False)
                    sqlinsert += " (%s,%s)"
                except KeyError:
                    errorString += items["symbol"] + ", "
            # finalize strings and query
            sqlinsert += ";"
            # only insert point if it doesnt exist
            # TODO: add try except
            DBcurr.execute(sqlinsert, sqlitems)
            connection.commit()
            # close cursor
            DBcurr.close()
            n = 0
            requestString = "("
        else:
            requestString += ", "
    if errorString == "":
        return "Success"
    else:
        return errorString

def updateStockInfo(connection):
    """
    updateStockInfo: updates stock info for stocks in database connection
    connection - database connection object
    return: success or error string
    """
    # get all stock names
    sqlQuery = "SELECT Symbol FROM StockInfo;"
    DBcurr = connection.cursor()
    DBcurr.execute(sqlQuery)
    haveList = DBcurr.fetchall()
    DBcurr.close()
    connection.commit()
    # for each stock
    n = 0
    t = 0
    tmax = len(haveList)
    requestString = "("
    errorString = ""
    for stocks in haveList:
        requestString += "'" + stocks[0] + "'"
        n += 1
        t += 1
        # check if request string is done
        if n == 16 or t == tmax:
            print(t)
            requestString += ")"
            # request json
            command = urllib.request.quote(u'select Stockholders,symbol from yahoo.finance.quant where symbol in ' + requestString)
            fetch = urllib.request.urlopen("http://query.yahooapis.com/v1/public/yql?q=" + command + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=").read()
            fetch = json.loads(fetch.decode("utf-8"))["query"]["results"]["stock"]
            # go through items and submit to sql server
            sqlitems = []
            sqlString = "UPDATE StockInfo SET Usable=TRUE WHERE symbol IN ("
            onItem = 0
            # iterate through fetched items
            for items in fetch:
                # only add to database if volume > 1mil
                try:
                    volume = items["Stockholders"]
                    if volume == None:
                        raise KeyError
                    volume = str(volume)
                    volume = volume.replace(',', '')
                    volume = volume.replace('(', '')
                    volume = volume.replace(')', '')
                    volume = int(volume)
                    # see if stock is wanted
                    if volume >= 50000:
                        sqlitems.append(items["symbol"])
                        # to format sting correctly
                        if onItem > 0:
                            sqlString += ","
                        sqlString += "%s"
                        onItem += 1
                except:
                    errorString += items["symbol"] + ", "
            sqlString += ");"
            if sqlitems:
                # open cursor
                # TODO: add try except
                DBcurr = connection.cursor()
                DBcurr.execute(sqlString, sqlitems)
                connection.commit()
                DBcurr.close()
            # get ready for next request
            n = 0
            requestString = "("
        else:
            requestString += ", "
    if errorString == "":
        return "Success"
    else:
        return errorString

def fetchStockCsv(symbol):
    """
    fetchStockCsv: fetches csv of historical data for stock symbol
    symbol - string symbol for stock
    return: boolean of success
    """
    try:
        urlPre = "http://real-chart.finance.yahoo.com/table.csv?s="
        urlMid = "&a=01&b=1&c=1962&d="
        urlEnd = "&g=d&ignore=.csv"
        # get end date for csv
        today = datetime.today().date()
        yearString = str(today.year)
        monthString = str(today.month - 1)
        dayString = str(today.day)
        url = urlPre + symbol + urlMid + monthString + "&e=" + dayString + "&f=" + yearString + urlEnd
        # fetch file
        urllib.request.urlretrieve(url, "./data/" + symbol + ".csv")
        return True
    except:
        return False

def deleteStock(symbol,connection):
    """
    deleteStock: deletes all stockpoints for stock symbol
    symbol - string symbol for stock
    connection - sql database connection object
    return: boolean of success
    """
    try:
        sqlDelete = "DELETE FROM StockPoints WHERE Symbol=%s;"
        sqlItems = [symbol]
        DBcurr = connection.cursor()
        DBcurr.execute(sqlDelete, sqlItems)
        DBcurr.close()
        connection.commit()
        return True
    except:
        return False

def fetchAllStocks(connection):
    """
    fetchAllStocks: fetches points for every stock being tracked
    connection - sql connection object
    return: success or error info
    """
    # get all stock names
    sqlQuery = "SELECT Symbol FROM StockInfo WHERE Usable=TRUE;"
    DBcurr = connection.cursor()
    DBcurr.execute(sqlQuery)
    haveList = DBcurr.fetchall()
    DBcurr.close()
    connection.commit()
    print(len(haveList))
    curr = 0
    errorString = ""
    # fetch each csv then add it to database
    for stocks in haveList:
        curr += 1
        tickerSymbol = stocks[0]
        print(curr, tickerSymbol)
        # check if stock data exists
        sqlQuery = "SELECT Symbol FROM StockPoints WHERE Symbol=%s;"
        sqlitem = [tickerSymbol]
        DBcurr = connection.cursor()
        DBcurr.execute(sqlQuery,sqlitem)
        haveData = DBcurr.fetchall()
        DBcurr.close()
        connection.commit()
        didFetch = False
        # only gather data if stock didnt exist
        if not haveData:
            didFetch = fetchStockCsv(tickerSymbol)
            if not didFetch:
                errorString += " Fetching " + tickerSymbol + ","
        if didFetch and not haveData:
            stockFileName = "data/" + tickerSymbol + ".csv"
            # open the file and read all points
            with open(stockFileName, 'r') as stockFile:
                csvRead = csv.reader(stockFile)
                csvRead.__next__()
                # initialize command
                sqlinsert = "INSERT INTO StockPoints (Symbol, Date, Open, High, Low, Close, Volume, AdjClose) VALUES "
                sqlitems = []
                onItem = 0
                # get points from file
                for rows in csvRead:
                    if onItem > 0:
                        sqlinsert += ","
                    onItem += 1
                    sqlitems.append(tickerSymbol)
                    sqlitems += rows
                    sqlinsert += " (%s,%s,%s,%s,%s,%s,%s,%s)"
                # Get Date for updated info
                Updated = datetime.today().date()
                changeItems = [Updated, tickerSymbol]
                changeDate = "UPDATE StockInfo SET EndDate=%s WHERE Symbol=%s"
                # TODO: add try except
                # Add points
                try:
                    DBcurr = connection.cursor()
                    DBcurr.execute(sqlinsert, sqlitems)
                    # Update Info
                    DBcurr.execute(changeDate, changeItems)
                    connection.commit()
                    DBcurr.close()
                except:
                    errorString += " Adding " + tickerSymbol + " to Database,"
            remove(stockFileName)
    if errorString == "":
        return "Success"
    else:
        return errorString

def updateStockPoints(connection):
    """
    updateStockPoints: adds all new stock points by checking max date and fetching historical data from then until today
    connection - database connection object
    return: string success or error info
    """
    errorString = ""
    # get all stock names
    sqlQuery = "SELECT MIN(EndDate) FROM StockInfo WHERE Usable=TRUE;"
    DBcurr = connection.cursor()
    DBcurr.execute(sqlQuery)
    minDate = DBcurr.fetchall()
    DBcurr.close()
    connection.commit()
    minDate = minDate[0][0]
    print(minDate)
    today = datetime.today().date()
    weekDay = today.weekday() - 4
    # if its a weekend treat today as friday
    if weekDay > 0:
        ntoday = today - timedelta(days=weekDay)
    else:
        ntoday = today
    # while min is not today
    while minDate < ntoday:
        # set last min as current min
        lastMinDate = minDate
        # get all stocks with current update date
        sqlQuery = "SELECT Symbol FROM StockInfo WHERE EndDate=%s AND Usable=TRUE;"
        sqlitem = [minDate]
        DBcurr = connection.cursor()
        DBcurr.execute(sqlQuery,sqlitem)
        updateList = DBcurr.fetchall()
        DBcurr.close()
        connection.commit()
        # find range and decide number to max at
        numStocks = len(updateList)
        dateDiff = today - minDate
        dayDiff = dateDiff.days
        # initialize for looped query
        nmax = int(250 / dayDiff)
        n = 0
        t = 0
        requestString = "("
        errorString = ""
        for stocks in updateList:
            requestString += "'" + stocks + "'"
            n += 1
            t += 1
            if n == nmax or t == numStocks:
                print(t)
                requestString += ")"
                # request json
                command = urllib.request.quote(u'select * from yahoo.finance.historicaldata where symbol in ' + requestString)
                fetch = urllib.request.urlopen("http://query.yahooapis.com/v1/public/yql?q=" + command + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=").read()
                fetch = json.loads(fetch.decode("utf-8"))["query"]["results"]["quote"]
                # go through items and submit to sql server
                sqlitems = []
                sqlinsert = "INSERT INTO StockPoints (Symbol, Date, Open, High, Low, Close, Volume, AdjClose) VALUES "
                sqlupdate = "UPDATE StockInfo SET EndDate=%s WHERE Symbol IN ("
                sqlupitem = [today]
                onItem = 0
                # get points from json
                for items in fetch:
                    try:
                        if onItem > 0:
                            sqlinsert += ","
                            sqlupdate += ","
                        onItem += 1
                        sqlitems.append(items["Symbol"])
                        sqlupitem.append(items["Symbol"])
                        sqlitems.append(items["Date"])
                        sqlitems.append(items["Open"])
                        sqlitems.append(items["High"])
                        sqlitems.append(items["Low"])
                        sqlitems.append(items["Close"])
                        sqlitems.append(items["Volume"])
                        sqlitems.append(items["Adj_Close"])
                        sqlinsert += " (%s,%s,%s,%s,%s,%s,%s,%s)"
                        sqlupdate += "%s"
                    except KeyError:
                        errorString += "Fetch: "+ items["Symbol"] + ", "
                sqlinsert += ";"
                sqlupdate += ");"
                # TODO: add try except
                #try:
                # commit points to database
                DBcurr = connection.cursor()
                DBcurr.execute(sqlinsert, sqlitems)
                DBcurr.execute(sqlupdate, sqlupitem)
                connection.commit()
                DBcurr.close()
                #except:
                #    errorString += "Error commiting to database"
                # reset for next group
                n = 0
                requestString = "("
            else:
                requestString += ", "
        sqlQuery = "SELECT MIN(EndDate) FROM StockInfo WHERE Usable=TRUE;"
        DBcurr = connection.cursor()
        DBcurr.execute(sqlQuery)
        minDate = DBcurr.fetchall()
        DBcurr.close()
        connection.commit()
        minDate = minDate[0][0]
        # if min date doesn't change then done
        if minDate == lastMinDate:
            break
    if errorString == "":
        return "Success"
    else:
        return errorString