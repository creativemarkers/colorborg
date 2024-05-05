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
        return recursiveTruncateRandGauss(mean,sigma,upperBound,lowerBound)

def iterativeTruncateRandGauss(mean,sigma,upperBound,lowerBound):
    while True:

        result = random.gauss(mean,sigma)
        if lowerBound <= result <= upperBound:
            return result

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
    mean = 0.0950
    sigma = .01
    lowerBound = 0.05
    upperBound = 0.250
    clicks = {}
    clickDurs = []

    # testRange,

    for i in range(100000):
        result = round(iterativeTruncateRandGauss(mean,sigma,upperBound,lowerBound),3)
        clickDurs.append(result)
        # if result not in clicks:
        #     clicks[result] = 1
        # else:
        #     clicks[result] +=1

    plt.hist(clickDurs, bins=20)
    plt.show()
    # print(clicks)
    # plt.bar(clicks.keys(),clicks.values(),align="center")
    # plt.show()

if __name__ == "__main__":
    main()