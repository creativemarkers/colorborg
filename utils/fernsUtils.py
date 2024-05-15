"""

(╭ರ_•́) A Gentle Mans' Utils (╭ರ_•́)
       by Fernando N Sanchez

"""

import random
import time

#recursively provides a random truncated number using standard/normal distribution
def recursiveTruncateRandGauss(mean,sigma,upperBound,lowerBound):
    result = random.gauss(mean,sigma)
    if lowerBound <= result <= upperBound:
        return result
    else:
        return recursiveTruncateRandGauss(mean,sigma,upperBound,lowerBound)

#iteratively provides a random truncated number using standard/normal distribution
def iterativeTruncateRandGauss(mean,sigma,upperBound,lowerBound):
    while True:

        result = random.gauss(mean,sigma)
        if lowerBound <= result <= upperBound:
            return result
        
#function timing decorator
def measureTime(func):
    def wrapper(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        print(f"{func.__name__} executed in {endTime - startTime} seconds")
        return result
    return wrapper


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

    import matplotlib.pyplot as plt  
    mean = 2
    sigma = 1.10
    lowerBound = .50
    upperBound = 6
    clicks = {}
    clickDurs = []

    # testRange
    @measureTime
    def testRange():
        for i in range(1000000):
            result = round(iterativeTruncateRandGauss(mean,sigma,upperBound,lowerBound))
            # clickDurs.append(result)
        
            if result not in clicks:
                clicks[result] = 1
            else:
                clicks[result] +=1
        print(clicks)

    # plt.hist(clickDurs, bins=20)
    # plt.show()
    # plt.bar(clicks.keys(),clicks.values(),align="center")
    # plt.show()

    testRange()

if __name__ == "__main__":
    main()