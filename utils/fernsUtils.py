"""
(╭ರ_•́) A Gentle Mans' Utils (╭ರ_•́)
       by Fernando N Sanchez
"""

import random
import time

def recursiveTruncateRandGauss(mean,sigma,upperBound,lowerBound):
    """
    Recursively Provides a random truncated number using standard/normal distribution
    """
    result = random.gauss(mean,sigma)
    if lowerBound <= result <= upperBound:
        return result
    else:
        return recursiveTruncateRandGauss(mean,sigma,upperBound,lowerBound)

def iterativeTruncateRandGauss(mean,sigma,upperBound,lowerBound):
    """
    Iteratively provides a random truncated number using standard/normal distribution
    """
    while True:

        result = random.gauss(mean,sigma)
        if lowerBound <= result <= upperBound:
            return result
        
def measureTime(func):
    """
    decorator function to measure the time a function took to execute
    best only to use during testing
    """
    def wrapper(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        print(f"{func.__name__} executed in {endTime - startTime} seconds")
        return result
    return wrapper

def calculateDaysSinceAD1(y:int=None,m:int=None,d:int=None,date:str=None)->int:
    """
    Calculates total dates since 1, 1, 1 AD
    Assumes date format "YYYY_MM_DD"
    No format checking on function so be wary
    """
    if date:
        splitDate = date.split("_")
        year = int(splitDate[0]) - 1
        month = int(splitDate[1])
        day = int(splitDate[2])
    else:
        year = y - 1
        month =  m
        day = d
        
    yearsInDays = (year * 365) + ((year//4)-(year//100)+(year//400))

    year += 1
    if year % 4 == 0:
        if not year % 100 == 0:
            yearsInDays += 1
        if year % 400 == 0:
            yearsInDays += 1
        
    amountOfDaysinMonth = {
        1:31, 2:28, 3:31, 4:30, 5:31, 6:30,
        7:31, 8:31, 9:30, 10:31, 11:30
    }
    
    monthsInDays = 0
    for i in range(1,month):
        if i in amountOfDaysinMonth:
            monthsInDays += amountOfDaysinMonth[i]
    return yearsInDays + monthsInDays + day
        
def main():
    """
           `
         `
         [ ]
         |`|  
        /  `\
       /~~~~~\
      (_______)
FOR THE MINDFUL TESTERS
    """

    # import matplotlib.pyplot as plt  
    # mean = 2
    # sigma = 1.10
    # lowerBound = .50
    # upperBound = 6
    # clicks = {}
    # clickDurs = []

    # # testRange
    # @measureTime
    # def testRange():
    #     for i in range(1000000):
    #         result = round(iterativeTruncateRandGauss(mean,sigma,upperBound,lowerBound))
    #         # clickDurs.append(result)
        
    #         if result not in clicks:
    #             clicks[result] = 1
    #         else:
    #             clicks[result] +=1
    #     print(clicks)

    # plt.hist(clickDurs, bins=20)
    # plt.show()
    # plt.bar(clicks.keys(),clicks.values(),align="center")
    # plt.show()

    result = calculateDaysSinceAD1("2024_06_07")
    
    print(result)
    # testRange()

if __name__ == "__main__":
    main()