import psycopg2

def dbLogin():
    """
    dbLogin: logs into database for stock market program
    return: sql connection object or failure boolean
    """
    try:
        return psycopg2.connect("dbname=StockMarket user=postgres password=mathmatician3")
    except:
        return False

def createTables(connection):
    """
    createTables: creates tables in database connection for stockmarket
    connection - sql connection object
    return: boolean success or fail
    """
    DBcurr = connection.cursor()
    success = True
    # try to create all database tables
    try:
        DBcurr.execute("CREATE TABLE StockInfo (Symbol varchar, StartDate date, EndDate date, Usable boolean);")
        # Unique index on Symbol to lookup
        DBcurr.execute("CREATE UNIQUE INDEX SymUIndex ON StockInfo (Symbol);")
        DBcurr.execute("CREATE INDEX EndIndex ON StockInfo (EndDate);")
        DBcurr.execute("CREATE TABLE StockPoints (Symbol varchar, Date date, Open float, High float, Low float, Close float, Volume float, AdjClose float);")
        # Index on Date and Symbol to lookup Symbol and filter on date
        DBcurr.execute("CREATE INDEX DateIndex ON StockPoints (Date);")
        DBcurr.execute("CREATE INDEX SymIndex ON StockPoints (Symbol);")
        connection.commit()
    except:
        connection.rollback()
        success = False
    # close cursor
    DBcurr.close()
    return success

def dropTables(connection):
    """
    dropTables: drops all tables that createTables creates
    connection - sql connection object
    return: boolean success or fail
    """
    DBcurr = connection.cursor()
    success = True
    # try to drop all database tables
    try:
        DBcurr.execute("DROP TABLE StockInfo;")
        DBcurr.execute("DROP TABLE StockPoints;")
        connection.commit()
    except:
        connection.rollback()
        success = False
    # close cursor
    DBcurr.close()
    return success

