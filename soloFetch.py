import csv
import urllib.request
import bs4


def fetchOneStock(ticker):
    urllib.request.urlretrieve("http://finance.yahoo.com/q/hp?s=" + ticker + "+Historical+Prices","TEMP.html")
    with open("TEMP.html", 'r') as stock:
        stockSoup = bs4.BeautifulSoup(stock)
    stockLink = stockSoup.find_all('p')[1].find_all('a')[0].get('href')
    urllib.request.urlretrieve(stockLink, "./data/" + ticker + ".csv")

fetchOneStock("AAPL")