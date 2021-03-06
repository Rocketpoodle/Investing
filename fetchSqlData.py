import initDB
import psycopg2
import time
from datetime import date

def getStockList(connection):
    """
    getStockList: returns the list of all stocks with their end date and usable values
    connection - sql database connection object
    return: list of stocks (stocks are list of their info values)
    """
    sqlString = "SELECT * FROM StockInfo WHERE Usable=TRUE ORDER BY Symbol"
    # open cursor
    DBcurr = connection.cursor()
    DBcurr.execute(sqlString)
    stocksList = DBcurr.fetchall()
    DBcurr.close()
    connection.commit()
    return stocksList

def getPoints(symbol, columns, connection):
    """
    getPoints: gets the points from sql database that has the columns listed in the array columns
    symbol - string symbol for stock
    columns - array with strings of column names
    connection - sql database connection object
    return: array of points (points are themselves an array)
    """
    queryString = ""
    onItem = 0
    # add columns to select
    for column in columns:
        if onItem > 0:
            queryString += ","
        onItem += 1
        queryString += column
    sqlString = "SELECT " + queryString + " FROM StockPoints WHERE Symbol=%s ORDER BY Date"
    sqlItem = [symbol]
    # open cursor
    DBcurr = connection.cursor()
    DBcurr.execute(sqlString, sqlItem)
    pointsList = DBcurr.fetchall()
    DBcurr.close()
    connection.commit()
    return pointsList

def priceQuery(symbol, date, connection):
    """
    priceQuery: gets the price of stock symbol at date date
    symbol - string symbol of stock to pricecheck
    connection - sql database connection object
    return: integer stock price
    """
    sqlString = "SELECT AdjClose FROM StockPoints WHERE Symbol=%s AND Date=%s;"
    sqlItem = [symbol, date]
    DBcurr = connection.cursor()
    DBcurr.execute(sqlString,sqlItem)
    try:
        price = DBcurr.fetchall()[0][0]
    except:
        price = False
    DBcurr.close()
    connection.commit()
    return price

def fetchBrokerInfo(name, connection):
    """
    fetchBrokerInfo: fetches info for broker name
    name - string name of broker
    connection - database connection object
    return: array of broker info
    """
    sqlString = "SELECT * FROM StockBroker WHERE Name=%s;"
    sqlItems = [name]
    brokerInfo = False
    # execute query
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString,sqlItems)
        brokerInfo = DBcurr.fetchone()
        DBcurr.close()
        connection.commit()
    except:
        connection.rollback()
        pass
    return brokerInfo

def setBrokerInfo(name, bank, date, connection):
    """
    setBrokerInfo: sets broker info for broker name
    name - string name of broker
    bank - float bankroll of broker
    date - date that broker is on
    connection - database connection object
    return: boolean of success
    """
    sqlString = "UPDATE StockBroker SET Bank=%s,Date=%s WHERE Name=%s;"
    sqlItems = [bank,date,name]
    # execute command
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString,sqlItems)
        connection.commit()
        DBcurr.close()
    except:
        connection.rollback()
        return False
    return True

def queryAllOwned(name, connection):
    """
    queryAllOwned: queries for all owned stocks for broker name
    name - string name of broker
    connection - database connection object
    return: list of symbol,shares for all owned stocks
    """
    sqlString = "SELECT Symbol,Shares FROM OwnedStocks WHERE Broker=%s;"
    sqlItems = [name]
    ownedStocks = []
    # execute command
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString,sqlItems)
        ownedStocks = DBcurr.fetchall()
        connection.commit()
        DBcurr.close()
    except:
        pass
    return ownedStocks

def queryLog(name, connection):
    """
    queryLog: queries for all log entries for name
    name - string name of broker
    connection - database connection object
    return: list of symbol,shares for all owned stocks
    """
    sqlString = "SELECT * FROM TransLog WHERE Broker=%s;"
    sqlItems = [name]
    ownedStocks = []
    # execute command
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString,sqlItems)
        ownedStocks = DBcurr.fetchall()
        connection.commit()
        DBcurr.close()
    except:
        pass
    return ownedStocks

def queryOwnedStock(name, symbol, connection):
    """
    queryOwnedStock: queries to see if stock is owned and how many
    name - string name of broker
    symbol - string symbol of stock to query for
    connection - database connection object
    return: total shares owned
    """
    sqlString = "SELECT Shares FROM OwnedStocks WHERE Broker=%s AND Symbol=%s;"
    sqlItems = [name, symbol]
    owned = 0
    # execute command
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString,sqlItems)
        owned = DBcurr.fetchone()[0]
        connection.commit()
        DBcurr.close()
    except:
        pass
    return owned

def clearTransLog(name, connection):
    """
    clearTransLog: clear transaction log for broker name
    name - string name of broker
    connection - database connection object
    return: boolean of success
    """
    sqlString = "DELETE FROM TransLog WHERE Broker=%s;"
    sqlItems = [name]
    # execute command
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString,sqlItems)
        connection.commit()
        DBcurr.close()
    except:
        connection.rollback()
        return False
    return True

def clearOwnedStocks(name, connection):
    """
    clearOwnedStocks: clear owned stocks for broker name
    name - string name of broker
    connection - database connection object
    return: boolean of success
    """
    sqlString = "DELETE FROM OwnedStocks WHERE Broker=%s;"
    sqlItems = [name]
    # execute command
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString,sqlItems)
        connection.commit()
        DBcurr.close()
    except:
        connection.rollback()
        return False
    return True

def sqlTransaction(date, name, buysell, symbol, shares, price, connection):
    """
    sqlTransaction: processes transaction on sql database
    name - string name of broker
    buysell - string buy or sell which denotes type of transaction
    shares - int number of shares to buy or sell
    price - float price of stock at buy
    connection - database connection object
    return: boolean of success
    """
    # initialize transaction string and items
    tranString = ""
    tranItems = []
    # initialize log string and items
    logString = "INSERT INTO TransLog (Date, Broker, Symbol, Shares, Price, BuySell) VALUES (%s,%s,%s,%s,%s,%s);"
    logItems = [date, name, symbol, shares, price, buysell]
    # check how much of the stock is owned
    owned = queryOwnedStock(name, symbol, connection)
    # buy transaction
    if buysell == "BUY":
        # if none are owned
        if owned == 0:
            tranString = "INSERT INTO OwnedStocks (Broker, Symbol, Shares) VALUES (%s,%s,%s);"
            tranItems = [name, symbol, shares]
        # if some are owned
        else:
            ownedVal = owned * price
            if ownedVal > 10000:
                return False
            tranString = "UPDATE OwnedStocks SET Shares=%s WHERE Broker=%s AND Symbol=%s;"
            newShares = owned + shares
            tranItems = [newShares, name, symbol]
    # sell transaction
    elif buysell == "SELL":
        # invalid if not enough shares are owned
        if shares > owned:
            return False
        # delete row if all shares sold
        elif shares == owned:
            tranString = "DELETE FROM OwnedStocks WHERE Broker=%s AND Symbol=%s;"
            tranItems = [name, symbol]
        # update row with remaining shares
        elif shares < owned:
            newShares = owned - shares
            tranString = "UPDATE OwnedStocks SET Shares=%s WHERE Broker=%s AND Symbol=%s;"
            tranItems = [newShares, name, symbol]
    # invalid transaction
    else:
        return False
    #try:
        # sql executions
    DBcurr = connection.cursor()
    DBcurr.execute(tranString,tranItems)
    connection.commit()
    DBcurr.execute(logString,logItems)
    connection.commit()
    DBcurr.close()
    #except:
        #return False
    return True

def dateExists(date, connection):
    """
    dateExists: queries for points on date to see if it exists
    date - date object to query
    connection - database connection object
    return: boolean if date exists
    """
    sqlString = "Select MAX(Date) FROM StockPoints WHERE Date=%s;"
    sqlItems = [date]
    # execute command
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString,sqlItems)
        dateNow = DBcurr.fetchone()
        connection.commit()
        DBcurr.close()
    except:
        connection.rollback()
        return False
    # check if date exists
    if dateNow:
        return True
    else:
        return False

def stockDateExists(date, symbol, connection):
    """
    dateExists: queries for points on date to see if it exists
    date - date object to query
    connection - database connection object
    return: boolean if date exists
    """
    sqlString = "Select MAX(Date) FROM StockPoints WHERE Date=%s AND Symbol=%s;"
    sqlItems = [date, symbol]
    # execute command
    try:
        DBcurr = connection.cursor()
        DBcurr.execute(sqlString, sqlItems)
        dateNow = DBcurr.fetchone()
        connection.commit()
        DBcurr.close()
    except:
        connection.rollback()
        return False
    # check if date exists
    if dateNow[0]:
        return True
    else:
        return False

def getPointsDateRange(d1, d2, symbol, columns, connection):
    """
    getPoints: gets the points from sql database that has the columns listed in the array columns
    d1, d2 - date range to load points from
    symbol - string symbol for stock
    columns - array with strings of column names
    connection - sql database connection object
    return: array of points (points are themselves an array)
    """
    queryString = ""
    onItem = 0
    # add columns to select
    for column in columns:
        if onItem > 0:
            queryString += ","
        onItem += 1
        queryString += column
    sqlString = "SELECT " + queryString + " FROM StockPoints WHERE Symbol=%s AND DATE BETWEEN %s AND %s ORDER BY Date"
    sqlItem = [symbol,d1,d2]
    # open cursor
    DBcurr = connection.cursor()
    DBcurr.execute(sqlString, sqlItem)
    pointsList = DBcurr.fetchall()
    DBcurr.close()
    connection.commit()
    return pointsList


