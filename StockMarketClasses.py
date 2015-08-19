__author__ = 'Austin'

class Company:

    def __init__(self, symbol, price, file):
        self.symbol = symbol
        self.price = price
        self.file = file

    def toString(self):
        printString = ""
        printString += self.symbol + "\n"
        printString += "Price: " + str(self.price) + "\n"
        printString += "Data File: " + self.file
        return printString


