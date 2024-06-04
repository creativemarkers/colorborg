import matplotlib.pyplot as plt
import pyautogui
import random
from utils.fernsUtils import recursiveTruncateRandGauss, measureTime

pyautogui.MINIMUM_DURATION = 0.0001
pyautogui.MINIMUM_SLEEP = 0.0001
pyautogui.PAUSE = 0.000001

class BezierMouse():
    PERCENT_MAXOFFSET = 10

    def getMaxDistance(self,p0, p2):

        p0x, p0y = p0
        p2x, p2y = p2
        xDist = abs(p0x-p2x)
        yDist = abs(p0y-p2y)
        return max(xDist,yDist)

    def calculateTincrement(self,p0, p2):

        tD = self.getMaxDistance(p0, p2)
        if tD <= 100:
            return 0.1
        elif tD <= 500:
            return 0.02
        else:
            return 0.01
        
    def calculateTravelSpeed(self,tD) -> float:
        """
        5-10px a millisecond
        average speed of a mouse movement is 100-250 inches per second the higher range being competive gaming
        assuming our mouse is set to 1000dpi
        usb polls at 1000hz
        the average human reaction time is 200ms for experienced gamers can be as low as 150ms for visual stimuli
        """
        randPXPerMS = recursiveTruncateRandGauss(9,1,11,4)
        #grabs total distance and divides it be px per microsecond, then converts to microseconds ex: 100/5 = 2.5/10000= 0.0025 <- final result in microseconds
        totalTravelTime = (tD/randPXPerMS)/10000
        print("total travel time:",totalTravelTime)
        return totalTravelTime

    def calculateOffSet(self,p0,p2):

        totalDistance = self.getMaxDistance(p0,p2)
        offSet = totalDistance / 5
        return offSet

    def determineMidPoint(self,p0,p2,offset):

        osx = random.gauss(0,offset)
        osy = random.gauss(0,offset)
        print(f"Offset X: {osx}, Offset Y: {osy}")

        p0x, p0y = p0
        p2x, p2y = p2

        x = ((p0x + p2x)/2) + osx
        y = ((p0y + p2y)/2) + osy

        return (x,y)
        
    def calculatelinearControlPoints(self,p0,p1,tIncrement):
        t = 0
        while t <= 1:
            p0t = tuple((1-t) * digit for digit in p0) 
            p1t = tuple(t * digit for digit in p1)
            b = tuple(a + b for a,b in zip(p0t, p1t))
            print(b)
            t += tIncrement

    # @measureTime
    def calculateQuadraticControlPoints(self, p0, p1, p2, tIncrement):
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

    def getOffsetPoint(self, start:tuple, end:tuple, ll:float=.01, ul:float=.99):
        #will pick a random point to start calculating the offset point
        """
        perhaps could determine this based on dista
        """
        t = random.uniform(ll,ul)
        startT = tuple(((1-t) * digit for digit in start))
        endT = tuple(t * digit for digit in end )
        res = tuple(a+b for a,b in zip(startT,endT))
        return res

    def getCubicControlPoints(self, p0,osp1,osp2,p3):
        """
        get distance
        the closer the total distance the less dramatic the offset could be
        https://homepages.bluffton.edu/~nesterd/apps/beziersketcher.html
        ^for messing around with the curves
        """
        mD = self.getMaxDistance(p0,p3)
        
        maxOffset = round(mD/self.PERCENT_MAXOFFSET)

        cp1 = tuple(random.randint((-1*(maxOffset)),maxOffset) + digit for digit in osp1)
        print("cp1",cp1)
        cp2 = tuple(random.randint((-1*(maxOffset)),maxOffset) + digit for digit in osp2)
        print("cp2",cp2)

        return cp1, cp2

    def calculateCubicControlPoints(self, p0,p3):
        #it doesn't actually matter where the offsetPoints are the more important thing is the amount offset off those points

        osp1 =  self.getOffsetPoint(p0,p3)
        print("osp1:",osp1)
        osp2 = self.getOffsetPoint(p0,p3)
        print("osp2:",osp2)
        p1,p2 = self.getCubicControlPoints(p0,osp1,osp2,p3)
        return p1,p2

    def moveMouseWithCubicCurve(self, dest, origin=None):
        if not origin:
            p0 = pyautogui.position()
        else:
            p0 = origin
        p1,p2 = self.calculateCubicControlPoints(p0,dest)
        tInc = self.calculateTincrement(p0,dest)
        cpArr = self.calculateCubicCurve(p0,p1,p2,dest,tInc)
        pArr = cpArr[:]
        dist = self.getMaxDistance(p0,dest)
        dur = self.calculateTravelSpeed(dist)
        self.moveMouseWithArray(cpArr = cpArr,totalDur = dur)

        # return p0, p1, p2, dest, pArr

    # @measureTime
    def calculateCubicCurve(self, p0,p1,p2,p3, tIncrement):
        t = 0
        bArr = []
        while t <= 1:
            p0t = tuple( ((1-t)**3)*digit for digit in p0 )
            p1t = tuple( ((((1-t)**2)*t)*3) * digit for digit in p1 )
            p2t = tuple( ((1-t)*(t**2))*3 * digit for digit in p2 )
            p3t = tuple( (t**3) * digit for digit in p3 )
            b = tuple( a+b+c+d for a,b,c,d in zip(p0t,p1t,p2t,p3t))
            # print(b)
            bArr.append(b)
            t += tIncrement
            t = round(t,2)
        return bArr

    # @measureTime
    def moveMouseWithArray(self, cpArr,totalDur):

        amountOfIters = len(cpArr)
        # print("steps:",amountOfIters)
        durPerIter = totalDur/amountOfIters
        durPerIter = round(durPerIter,5)
        # print("dur per iter:",durPerIter)
        while cpArr:
            cords = cpArr.pop(0)
            x,y = cords
            x = round(x)
            y = round(y)
            # @measureTime
            def moveM(x,y,durPerIter):
                pyautogui.moveTo(x,y,durPerIter)
            moveM(x,y,durPerIter)

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

    # # p0 = (100,100)
    # # p2 = (140,140)

    # p0 = (100,100)
    # p2 = (1500,100)

    # td = getMaxDistance(p0,p2)
    # dur = calculateTravelSpeed(td)
    # print("travelSpeed:", dur)
    # tI = calculateTincrement(p0,p2)

    # os = calculateOffSet(p0,p2)
    # m = determineMidPoint(p0,p2,os)
    # # m = (4,8)

    # os = calculateOffSet(p0,p2)
    # p1 = determineMidPoint(p0,p2,os)

    # os = calculateOffSet(p0,p2)
    # p2 = determineMidPoint(p0,p2,os)

    # result = calculateQuadraticControlPoints(p0,m,p2,tI)
    # moveMouseWithArray(result,dur)


    # val = getOffsetPoint((900,900),(1000,1000))
    # print(val)

    # r = calculateCubicCurve((0,0),(1,2),(3,3),(4,0),0.25)
    # print(r)
    bM = BezierMouse()
    p0,p1,p2,p3,result = bM.moveMouseWithCubicCurve((501,501),(1,1))
    print(result[-1])
    # print(result)
    # p0 = (0, 0)
    # p1 = (1, 2)
    # p2 = (3, 3)
    # p3 = (4, 0)
    # result = [(0, 0), (1, 1.5), (2, 2.25), (3, 1.5), (4, 0)]

    
    x_coords = [point[0] for point in result]
    y_coords = [point[1] for point in result]

    fig , ax = plt.subplots()
    ax.plot(x_coords, y_coords, label='Quadratic Bézier Curve')

    ax.scatter(*zip(*[p0, p1, p2, p3]), color='red', label='Control Points')  # Plot the control points

    ax.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Quadratic Bézier Curve')
    plt.show()

if __name__ == "__main__":
    main()