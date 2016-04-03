import initDB
import psycopg2

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

def getPointsDateRange(d1, d2, connection):
    """
    getPointsDateRange: gets points for dates between d1 and d2 from connection
    d1, d2 - date objects
    connection - database connection object
    return: list of stock point lists
    """
    # query for all tickers within range
    sqlString = "SELECT DISTINCT Symbol FROM StockPoints WHERE Date BETWEEN %s AND %s;"
    sqlItem = [d1,d2]
    DBcurr = connection.cursor()
    DBcurr.execute(sqlString,sqlItem)
    nameList = DBcurr.fetchall()
    # get data for those tickers within that range
    stockRanges = []
    for names in nameList:
        symbol = names[0]
        sqlString = "SELECT * FROM StockPoints WHERE Symbol = %s AND Date BETWEEN %s AND %s ORDER BY Date;"
        sqlItem = [symbol, d1, d2]
        # get all points for the symbol and date range
        DBcurr.execute(sqlString,sqlItem)
        stockRanges.append(DBcurr.fetchall())
    DBcurr.close()
    connection.commit()
    return stockRanges

def priceQuery(symbol, date, connection):
    """
    priceQuery: gets the price of stock symbol at date date
    symbol - string symbol of stock to pricecheck
    connection - sql database connection object
    return: integer stock price
    """
    sqlString = "SELECT Close FROM StockPoints WHERE Symbol=%s AND Date=%s;"
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

def fetchBrokerInfo(broker, connection):
    """
    fetchBrokerInfo: fetches broker info from connection
    broker - string name for broker
    connection - db connection object
    return: broker info
    """
    sqlString = "SELECT * FROM StockBroker WHERE Name=%s;"
    sqlItem = [broker]
    DBcurr = connection.cursor()
    DBcurr.execute(sqlString,sqlItem)
    try:
        info = DBcurr.fetchall()
    except:
        info = False
    return info
