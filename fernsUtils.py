"""

(╭ರ_•́) A Gentle Mans' Utils (╭ರ_•́)
       by Fernando N Sanchez

"""

import random

def recursiveTruncateRandGauss(mean,sigma,upperBound,lowerBound):
    result = random.gauss(mean,sigma)
    if lowerBound <= result <= upperBound:
        return result
    else:
        print("out of bounds")
        return recursiveTruncateRandGauss(mean,sigma,upperBound,lowerBound)

def iterativeTruncateRandGauss(mean,sigma,upperBound,lowerBound):
    while True:

        result = random.gauss(mean,sigma)
        if lowerBound <= result <= upperBound:
            return result
        print("out of bounds")

def main():
    #testing function
    mean = 0
    sigma = 1
    lowerBound = -0.5
    upperBound = 0.5

    result = iterativeTruncateRandGauss(mean,sigma,upperBound,lowerBound)
    print(result)

if __name__ == "__main__":
    main()