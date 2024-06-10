import matplotlib.pyplot as plt
import pyautogui
import random
import logging
from utils.fernsUtils import recursiveTruncateRandGauss, measureTime

logger = logging.getLogger(__name__)

class BezierMouse():
    """
    PERCENT_MAXOFFSET 
        controls the amount of curve the mouse path will have
    TRAVELTIME_DIVISOR 
        determines the overall speed of the mouse along it's path, 
        the lower the number the slower the path
    """
    PERCENT_MAXOFFSET= 10
    TRAVELTIME_DIVISOR = 4000
    
    def __init__(self):
        pyautogui.MINIMUM_DURATION = 0.0001
        pyautogui.MINIMUM_SLEEP = 0.0001
        pyautogui.PAUSE = 0.000001

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
        randPXPerMS = recursiveTruncateRandGauss(2,1,5,1)
        #grabs total distance and divides it be px per microsecond, then converts to milliseconds ex: 100/5 = 2.5/10000= 0.0025 <- final result in microseconds
        totalTravelTime = (tD/randPXPerMS)/self.TRAVELTIME_DIVISOR
        # print("total travel time:",totalTravelTime)
        return totalTravelTime

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
        # print("cp1",cp1)
        cp2 = tuple(random.randint((-1*(maxOffset)),maxOffset) + digit for digit in osp2)
        # print("cp2",cp2)

        return cp1, cp2

    def calculateCubicControlPoints(self, p0,p3):
        #it doesn't actually matter where the offsetPoints are the more important thing is the amount offset off those points
        osp1 =  self.getOffsetPoint(p0,p3)
        # print("osp1:",osp1)
        osp2 = self.getOffsetPoint(p0,p3)
        # print("osp2:",osp2)
        p1,p2 = self.getCubicControlPoints(p0,osp1,osp2,p3)
        return p1,p2

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

    @measureTime
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

        logger.debug("successfully moved mouse along array")
        
    def moveMouseWithCubicCurve(self, dest, origin=None):
        # print("pyautogui constant from bezier")
        pyautogui.MINIMUM_DURATION = 0.0001
        pyautogui.MINIMUM_SLEEP = 0.0001
        pyautogui.PAUSE = 0.000001
        logger.debug("changed pyautogui constants")
        # print(pyautogui.MINIMUM_DURATION)
        # print(pyautogui.MINIMUM_SLEEP)
        # print(pyautogui.PAUSE)
        if not origin:
            logger.debug("no origin position given for the mouse, getting current mouse position")
            p0 = pyautogui.position()
        else:
            logger.debug("origin position was given")
            p0 = origin

        logger.debug("calculating control points")
        p1,p2 = self.calculateCubicControlPoints(p0,dest)

        logger.debug("calculating T increment")
        tInc = self.calculateTincrement(p0,dest)

        logger.debug("culculating cubic curve")
        cpArr = self.calculateCubicCurve(p0,p1,p2,dest,tInc)
    
        logger.debug("getting distance to determine travel time")
        dist = self.getMaxDistance(p0,dest)

        logger.debug("calculating travel time")
        dur = self.calculateTravelSpeed(dist)

        logger.debug("moving mouse with the cubic curve array")
        self.moveMouseWithArray(cpArr = cpArr,totalDur = dur)

def main():
    pass
if __name__ == "__main__":
    main()