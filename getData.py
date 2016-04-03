import urllib.request
import json
import initDB
import csv
from datetime import date,datetime
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
        if n == 250 or t == tmax:
            print(t)
            requestString += ")"
            # open cursor
            DBcurr = connection.cursor()
            # request json
            command = urllib.request.quote(u'select * from yahoo.finance.stocks where symbol in '+ requestString)
            fetch = urllib.request.urlopen("http://query.yahooapis.com/v1/public/yql?q=" + command +"&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=").read()
            fetch = json.loads(fetch.decode("utf-8"))["query"]["results"]["stock"]
            # go through items and submit to sql server
            sqlinsert = "INSERT INTO StockInfo (Symbol, StartDate, EndDate, Usable) VALUES"
            sqlitems = []
            onItem = 0
            # iterate through fetched items
            for items in fetch:
                try:
                    # check if start and end dates are valid
                    trial = items["start"].split("-")
                    if "NaN" == trial[1]:
                        items["start"] = trial[0] + "01" + trial[2]
                    trial = items["end"].split("-")
                    if "NaN" == trial[1]:
                        items["start"] = trial[0] + "01" + trial[2]
                    # insert comma when needed
                    if onItem > 0:
                        sqlinsert += ","
                    onItem += 1
                    # commit info to local sql server
                    sqlitems.append(items["symbol"])
                    sqlitems.append(items["start"])
                    sqlitems.append(items["end"])
                    sqlitems.append(False)
                    sqlinsert += " (%s,%s,%s,%s)"
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
                    volume = volume.replace(',','')
                    volume = volume.replace('(','')
                    volume = volume.replace(')','')
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
                    errorString += items["symbol"]
            sqlString += ");"
            if sqlitems:
                # open cursor
                # TODO: add try except
                DBcurr = connection.cursor()
                DBcurr.execute(sqlString,sqlitems)
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
        DBcurr.execute(sqlDelete,sqlItems)
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
    # fetch each csv then add it to database
    for stocks in haveList:
        tickerSymbol = stocks[0]
        didFetch = fetchStockCsv(tickerSymbol)
        if didFetch:
            stockFileName = "data/" + tickerSymbol + ".csv"
            # open the file and read all points
            with open(stockFileName,'r') as stockFile:
                csvRead = csv.reader(stockFile)
                csvRead.__next__()
                #initialize command
                sqlinsert = "INSERT INTO StockPoints (Symbol, Date, Open, High, Low, Close, Volume, AdjClose) VALUES "
                sqlitems = []
                onItem = 0
                # get points from file
                for rows in csvRead:
                    if onItem > 0:
                        sqlinsert += ","
                    onItem += 1
                    sqlitems += tickerSymbol
                    sqlitems += rows
                    sqlinsert += " (%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sqlitems)
                # Get Date for updated info
                Updated = datetime.today().date()
                changeItems = [Updated,tickerSymbol]
                changeDate = "UPDATE StockInfo SET EndDate=%s WHERE Symbol=%s"
                # TODO: add try except
                # Add points
                DBcurr = connection.cursor()
                DBcurr.execute(sqlinsert,sqlitems)
                # Update Info
                DBcurr.execute(changeDate,changeItems)
                connection.commit()
                DBcurr.close()
            remove(stockFileName)
connection = initDB.dbLogin()
#print(updateStockInfo(connection))
#fetchAllStocks(connection)
deleteStock("A",connection)