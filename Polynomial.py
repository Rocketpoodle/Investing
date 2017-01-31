import cmath

class Polynomial(object):
    """Polinomial class contains coefficients and can evaluate itself
    and find its derivative. Also it can evaluate an array of points."""
        
    coefficients = []
    degree = 0

    def __init__(self, coeff = []):
        x=0
        for x in range(0, len(coeff)): # strip leading 0 coefficients
            if coeff[x] != 0:
                break
        self.coefficients = coeff[x:]
        self.degree = (len(coeff) - x)-1 # save degree
        if self.degree < 0: # check if polynomial has no coefficients
            raise ValueError("Empty Polynomial") 

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
        else:
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
        for x in range (0,self.degree):
            derivCoeff.append(self.coefficients[x]*(self.degree - x))
        deriv = Polynomial(derivCoeff)
        return deriv

    def __str__(self):
        """creates string representation for polynomial"""
        polyStr = ""
        # step through all coefficients
        for x in range (0, self.degree+1):
            # dont print if 0
            if self.coefficients[x] == 0:
                polyStr += ""
            else:
                if x != 0:
                    polyStr += " + "    # add plus sign if not first
                polyStr += str(self.coefficients[x]) #add coefficient value
                if x < (self.degree):
                    polyStr += "x"  # add x if not constant term
                if x < (self.degree - 1):
                    polyStr += "^"  # add power if not degree 1 or constant term
                    polyStr += str(self.degree - x)
        return polyStr

    def deflate(self, root, strict = False):
        """deflates polynomial using root. Returns deflated polynomial"""
        newcoeffs = []
        value = 0
        for x in range(0, self.degree): # synthetic division
            value += self.coefficients[x]
            newcoeffs.append(value)
            value *= root
        value += self.coefficients[self.degree]
        if value != 0 and strict: # check for valid deflation
            raise ValueError("Not a valid root, Cannot Deflate")
        return Polynomial(newcoeffs) # return deflated polynomial

    def getRoots(self,value = 0, real = False, maxIters = 10):
        """solves for roots using laguerres method. Set value to change what y value it finds roots for.
        Real sets wether or not to only return real roots (returns them as float)"""
        roots = []
        currpoly = Polynomial(self.coefficients) # start as self as current polynomial
        currpoly.coefficients[self.degree] -= value # shift value to solve for
        while(currpoly != None):
            if currpoly.degree == 1: # linear
                roots.append((0 - currpoly.coefficients[1]) / currpoly.coefficients[0])
                break # done finding roots
            elif currpoly.degree == 2: # quadratic
                twoa = 2*currpoly.coefficients[0]
                sqrtbac = (cmath.sqrt((currpoly.coefficients[1]*currpoly.coefficients[1]) - 4*currpoly.coefficients[0]*currpoly.coefficients[2]) / twoa)
                b2a = (0 - currpoly.coefficients[1])/(twoa)
                roots.append(b2a + sqrtbac)
                roots.append(b2a - sqrtbac)
                break # done finding roots
            else:
                root = 0 # initialize root
                alpha = 1 # starting alpha at 0
                lalpha = [2,3]
                dp = currpoly.differentiate() # get derivative
                ddp = dp.differentiate() # get second derivative
                iters = 0
                while(abs(alpha) > 2e-17 and iters < maxIters):
                    iters += 1
                    p = currpoly.evaluate(root) # get polynomial value at root
                    pp = dp.evaluate(root) # get derivative at root
                    ppp = ddp.evaluate(root) # get second derivative at root
                    if p == 0: # if p is 0 then root is found
                        break
                    G = (pp / p)
                    Gsqr = G*G
                    H = Gsqr - (ppp / p)
                    sqrtHG = cmath.sqrt((currpoly.degree - 1)*(currpoly.degree*H - Gsqr))
                    denom1 = G + sqrtHG
                    denom2 = G - sqrtHG
                    if abs(denom1) > abs(denom2): # choose largest magnitude denominator
                        alpha = currpoly.degree / denom1
                    else:
                        alpha = currpoly.degree / denom2
                    root -= alpha # update root
                currpoly = currpoly.deflate(root) # deflate polynomial
                roots.append(root) # store root
                if root.imag != 0: # check if root was complex
                    conj = root.conjugate() # get conjugate
                    currpoly = currpoly.deflate(conj) # deflate polynomial again
                    roots.append(conj) # store conjugate root
        if real: # if real roots are requested
            realroots = []
            for root in roots:
                if root.imag == 0: # checks if real
                    realroots.append(root.real)
            roots = realroots
        return roots # return sorted roots