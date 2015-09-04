__author__ = 'rocketpoodle'

#=============================================#
#============== DEFINE FORMULA ===============#
#=============================================#

#Todo define worth formula with coefficients
# coefficients range from -1 to 1 and are addative (pending change)
# coefficient values are stored in Coefficients.txt as each line in style 'CoefficientName' = CoefficientValue
# explore all possible coefficients available

#Todo define 'arbitrary' sell and buy points
# buy and sell points based upon worth vs market values


def refineCoefficient():
# refine coefficient between -1 and 1 to maximize total profit
# steps through -1 to 1 and runs stock market and checks change in profit
# utilize runTimeFrame to find profit over time frame

def runTimeFrame(startDate,endDate):
# runs market from startDate to endDate, checks if contains both to find if valid
# place year in front of date to create sorting value for data point
# buys and sells stocks when they hit buy and sell points
# returns profit