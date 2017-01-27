class Polynomial(object):
    """Polinomial class contains coefficients and can evaluate itself
    and find its derivative. Also it can evaluate an array of points."""
        
    coefficients = []
    degree = 0

    def __init__(self, coeff = []):
        self.coefficients = coeff
        self.degree = len(coeff)

    def evaluate(self, x):
        """evaluates polynomial at x using Horners factorizaiton"""
        # list evaluation
        if type(x) is list:
            evalarr = [] # start with blank list
            for y in x:
                value = 0 # reset evalueation value
                #Horners factorization
                for c in self.coefficients:
                    value *= y
                    value += c
                evalarr.append(value) # append new value
            return evalarr

        # single evaluation
        if type(x) is int or type(x) is float:
            value = 0 # reset evalueation value
            #Horners factorization
            for c in self.coefficients:
                value *= x
                value += c
            return value

    def differentiate(self):
        """returns polynomial class of derivative"""
        # create new array of coefficients
        derivCoeff = []
        for x in range (0,self.degree - 1):
            derivCoeff.append(self.coefficients[x]*((self.degree - x) - 1))
        deriv = Polynomial(derivCoeff)
        return deriv

    def __str__(self):
        """creates string representation for polynomial"""
        polyStr = ""
        # step through all coefficients
        for x in range (0, self.degree):
            # dont print if 0
            if self.coefficients[x] == 0:
                polyStr += ""
            else:
                if x != 0:
                    polyStr += " + "    # add plus sign if not first
                polyStr += str(self.coefficients[x]) #add coefficient value
                if x < (self.degree - 1):
                    polyStr += "x"  # add x if not constant term
                if x < (self.degree - 2):
                    polyStr += "^"  # add power if not degree 1 or constant term
                    polyStr += str((self.degree - x) - 1)
        return polyStr