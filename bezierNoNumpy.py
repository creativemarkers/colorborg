import matplotlib.pyplot as plt
import pyautogui
import random
from utils.fernsUtils import recursiveTruncateRandGauss, measureTime

# pyautogui.MINIMUM_DURATION = 0.0001
# pyautogui.PAUSE = 0.0001

def getTotalDistance(p0, p2):

    p0x, p0y = p0
    p2x, p2y = p2

    return abs(p0x-p2x) + abs(p0y-p2y)

def calculateTincrement(p0, p2):

    tD = getTotalDistance(p0, p2)
    if tD <= 100:
        return 0.1
    elif tD <= 500:
        return 0.02
    else:
        return 0.01
    
def calculateTravelSpeed(tD) -> float:
    """
    5-10px a millisecond
    average speed of a mouse movement is 100-250 inches per second the higher range being competive gaming
    assuming our mouse is set to 1000dpi
    usb polls at 1000hz
    the average human reaction time is 200ms for experienced gamers can be as low as 150ms for visual stimuli
    """
    randPXPerMS = recursiveTruncateRandGauss(7.5,1,11,4)
    #grabs total distance and divides it be px per microsecond, then converts to microseconds ex: 100/5 = 2.5/10000= 0.0025 <- final result in microseconds
    totalTravelTime = (tD/randPXPerMS)/10000
    print("total travel time:",totalTravelTime)
    return totalTravelTime
def calculateOffSet(p0,p2):

    totalDistance = getTotalDistance(p0,p2)
    offSet = totalDistance / 5
    return offSet

def determineMidPoint(p0,p2,offset):

    osx = random.gauss(0,offset)
    osy = random.gauss(0,offset)
    print(f"Offset X: {osx}, Offset Y: {osy}")

    p0x, p0y = p0
    p2x, p2y = p2

    x = ((p0x + p2x)/2) + osx
    y = ((p0y + p2y)/2) + osy

    return (x,y)
    
def calculateQuadraticControlPoints(p0, p1, p2, tIncrement):
    t = 0
    bArr = []
    while t <= 1:
        p0t = tuple( ((1-t)**2) * digit for digit in p0 )
        p1t = tuple( ((2*(1-t))*t) * digit for digit in p1 )
        p2t = tuple( (t**2) * digit for digit in p2 )
        b = tuple( a+b+c for a,b,c in zip(p0t,p1t,p2t))
        # print(b)
        bArr.append(b)
        t += tIncrement
    return bArr

def calculatelinearControlPoints(p0,p1,tIncrement):
    t = 0
    while t <= 1:
        p0t = tuple((1-t) * digit for digit in p0) 
        p1t = tuple(t * digit for digit in p1)
        b = tuple(a + b for a,b in zip(p0t, p1t))
        print(b)
        t += tIncrement

@measureTime
def moveMouseWithArray(cpArr,totalDur):
    pyautogui.MINIMUM_DURATION = 0.00001
    pyautogui.MINIMUM_SLEEP = 0.0001
    pyautogui.PAUSE = 0.000001

    amountOfIters = len(cpArr)
    print("steps:",amountOfIters)
    durPerIter = totalDur/amountOfIters
    durPerIter = round(durPerIter,4)
    print("dur per iter:",durPerIter)
    while cpArr:
        cords = cpArr.pop(0)
        x,y = cords
        x = round(x)
        y = round(y)
        pyautogui.moveTo(x,y,durPerIter)

def main():

    """
    distance  | increment
    000 - 100 | 0.10 (10cp)
    101 - 500 | 0.02 (50cp)
    500+ - inf| 0.01 (100cp)

    need a function that can handle the speed based on distance since less increments can make stuff look unnhuman

    would want variablespeed - the move function could handle the speed and divide it amonst the control points
    and multiple curves
    for more precise clicks a different type of algorithm would need to be used
    """

    # p0 = (100,100)
    # p2 = (140,140)

    p0 = (100,100)
    p2 = (1500,100)

    td = getTotalDistance(p0,p2)
    dur = calculateTravelSpeed(td)
    print("travelSpeed:", dur)
    tI = calculateTincrement(p0,p2)

    os = calculateOffSet(p0,p2)
    m = determineMidPoint(p0,p2,os)
    # m = (4,8)

    result = calculateQuadraticControlPoints(p0,m,p2,tI)

    moveMouseWithArray(result,dur)
    
    # x_coords = [point[0] for point in result]
    # y_coords = [point[1] for point in result]

    # fig , ax = plt.subplots()
    # ax.plot(x_coords, y_coords, label='Quadratic Bézier Curve')

    # ax.scatter(*zip(*[p0, m, p2]), color='red', label='Control Points')  # Plot the control points

    # ax.legend()
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.title('Quadratic Bézier Curve')
    # plt.show()


if __name__ == "__main__":
    main()