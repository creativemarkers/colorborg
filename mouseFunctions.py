import pyautogui
import cv2
import time
import random
from pyautogui import ImageNotFoundException
import numpy
import os
import logging
from utils.fernsUtils import recursiveTruncateRandGauss
from bezierNoNumpy import BezierMouse as bm
from utils.fernsUtils import measureTime

pyautogui.MINIMUM_DURATION = 0.01
#just brought in the below too CONSTANTS
pyautogui.MINIMUM_SLEEP = 0.01
pyautogui.PAUSE = 0.01

logger = logging.getLogger(__name__)

class Mouse:

    def __init__(self):
        pyautogui.FAILSAFE = True
        self.bezierMouse = bm()
        pyautogui.MINIMUM_DURATION = 0.01
        pyautogui.MINIMUM_SLEEP = 0.01
        pyautogui.PAUSE = 0.01

    @measureTime
    def moveMouseToArea(self, x:int, y:int, duration=1, areaVariance:int = 0, click:bool=False, bezier:bool = False):
        # print(duration)
        xVaried = x
        yVaried =  y

        if areaVariance > 0:
            xVaried, yVaried = self.addVariance(x, y, areaVariance)

        if not bezier:

            print("MOVING MOUSE LINEARLY")
            logger.info("moving mouse linearly")
            self.moveMouse(xVaried, yVaried, duration)
        else:
            print("MOVING MOUSE WITH CURVE")
            logger.info("moving mouse along bezier curve")
            self.bezierMouse.moveMouseWithCubicCurve((xVaried, yVaried))
            logger.debug("setting pyautogui constants back to original")
            pyautogui.MINIMUM_DURATION = 0.01
            pyautogui.MINIMUM_SLEEP = 0.01
            pyautogui.PAUSE = 0.01

        if click == True:
            self.mouseClick(xVaried,yVaried)

        return xVaried, yVaried  
    
    @measureTime                     
    def moveMouse(self, x:int, y:int, duration=1):
        
        tweeningList = [
            pyautogui.easeInQuad,
            pyautogui.easeOutQuad,
            pyautogui.easeInOutQuad,
            pyautogui.easeInBounce,
            pyautogui.easeInElastic
        ]

        #might not be random enough
        willTween = random.randrange(0,10)

        if willTween >= 6:
            #print(duration)
            pyautogui.moveTo(x,y, duration, random.choice(tweeningList))
        else:
            #print(duration)
            pyautogui.moveTo(x, y, duration)

    def addVariance(self, x:int, y:int, varianceAmount:int):
        #could add better randomness
        if varianceAmount <= 0:
            #logging.exception("ValueError")
            raise ValueError("Variance must be greater than 0")
        
        xCeilingVariance = x + varianceAmount
        xFloorVariance = x - varianceAmount

        yCeilingVariance = y + varianceAmount
        yFloorVariance = y - varianceAmount

        xVaried = random.randint(xFloorVariance,xCeilingVariance)
        yVaried = random.randint(yFloorVariance,yCeilingVariance)

        return xVaried, yVaried

    def durationVariance(self, x, y, duration):

        
        currentX, currentY = pyautogui.position()

        distanceX = abs(x - currentX)
        distanceY = abs(y - currentY)

        totalDistance = (distanceX+distanceY)/2

        #controls the speed lowering the floor will make the duration slower
        calcedDuration = float(duration * (totalDistance/random.randrange(800,1700)))

        if calcedDuration < 0.05:
            return 0.05
        else:
            return calcedDuration
        
    def findImageSimple(self, imageTofind:str, w = 687, h= 725 ,desiredConfidence = .9):
        
        try:
            # example call findImageSimple('img/test.png', .9)

            #ss = pyautogui.screenshot(region=(0,0, 892, 892))

            imageLocation = pyautogui.locateOnScreen(imageTofind, region=(0,0, w, h), confidence=desiredConfidence)
            #imageLocationCenter = pyautogui.center(imageLocation)
            x , y = pyautogui.center(imageLocation)
            # x, y = imageLocationCenter

            logger.info(f"MOUSEFUNCTIONS:FINDIMAGESIMPLE: found center of image:{x},{y}")

            return x , y
        except ImageNotFoundException:
            #logging.exception("ImageNotFoundException")
            raise ImageNotFoundException
        
    def findImageIteratively(self, imageToFind:str, maxCords:tuple=(687,725), expandAmount:int = 100,startConfidence = .9, floorConfidence = .5):

        def expandImageRegion(tLx,tLy,bRx,bRy):
            maxX,maxY = maxCords

            if tLx <= 0 and tLy <= 0 and bRx >= maxX and bRy >= maxY:
                return False
            
            if tLx >= 0:
                tLx -= expandAmount
                if tLx < 0:
                    tLy = 0
            if tLy >= 0:
                tLy -= expandAmount
                if tLy < 0:
                    tLy = 0

            if bRx < maxX:
                bRx += expandAmount
                if bRx > maxX:
                    bRx = maxX
            if bRy < maxY:
                bRy += expandAmount
                if bRy > maxY:
                    bRy = maxY

            return tLx,tLy,bRx,bRy

        maxed = False
        tLX,tLY = 400,400
        bRX, bRY = 500,500
        sizeX = bRX - tLX
        sizeY = bRY - tLY
        screenShotRegion = (tLX,tLY,sizeX,sizeY)
        i = 0

        while not maxed:
            #print(f"region attempt #{i}")
            curConf = startConfidence
            # k = 0
            while curConf >= floorConfidence:
                #print(f"conf attempt #{k}, current conf: {curConf}, screenShotRegion: {screenShotRegion}")
                try:
                    imageLocation = pyautogui.locateOnScreen(imageToFind, region=screenShotRegion, confidence=curConf)
                    x,y = pyautogui.center(imageLocation)
                    return x,y
                except ImageNotFoundException:
                    logger.debug(f"could not find image with confidence set at {curConf}, lowering it by .1")
                curConf -= 0.1
                # k +=1
                
            if expandImageRegion(tLX,tLY,bRX,bRY) == False:
                logger.debug("whole screen checked couldn't find image raising ImageNotFoundException")
                raise ImageNotFoundException
            else:
                tLX,tLY,bRX,bRY = expandImageRegion(tLX,tLY,bRX,bRY)
                sizeX = bRX - tLX
                sizeY = bRY - tLY
                screenShotRegion = (tLX,tLY,sizeX,sizeY)
                i += 1

    # @measureTime
    def findColorsFast(self, colorToFind:tuple, desiredRegion:tuple):
        #note!!! the elements in matching pixels are reversed so instead of getting x,y it gives us y,x
        #this method searches pixels left to right, bad for human likeness and overall behavior

        im = pyautogui.screenshot(region=desiredRegion)

        #converts images to a numpyArray
        imArr = numpy.array(im)

        #returns all matching pixel awful for speed
        matchingPixels = numpy.argwhere(numpy.all(imArr == colorToFind, axis=-1))

        return matchingPixels
    
    def findColorsRandomly(self, colorToFind:tuple, desiredRegion:tuple):
        #note!!! the elements in matching pixels are reversed so instead of getting x,y it gives us y,x

        im = pyautogui.screenshot(region=desiredRegion)

        #converts images to a numpyArray
        imArr = numpy.array(im)

        #does what it says on the tin, randomly generates row col and numbers to search the pixels randomly
        height, width, _ = imArr.shape
        randomRow = numpy.random.randint(0, height, size = (height, width))
        randomCol = numpy.random.randint(0, width, size=(height, width))

        #breaks once it finds one missing pixel(can be a bit too fast)
        matchingPixel = []
        for row, col in zip(randomRow.flat, randomCol.flat):
            if numpy.all(imArr[row,col]==numpy.array(colorToFind)):
                matchingPixel.append((row,col))
                break
        return matchingPixel
    
    # @measureTime
    def findColorsIteratively(self, colorToFind:tuple, maxCords:tuple=(687,725), expandAmount:int=100):
        """
        taking a long time with find colorsRandomly approximately(1-1.5seconds worst case)
        using fast cuts down time to average around 100ms-200ms
        """
        def expandImageRegion(tLx,tLy,bRx,bRy):
            maxX,maxY = maxCords

            if tLx <= 0 and tLy <= 0 and bRx >= maxX and bRy >= maxY:
                return False
            
            if tLx >= 0:
                tLx -= expandAmount
                if tLx < 0:
                    tLy = 0
            if tLy >= 0:
                tLy -= expandAmount
                if tLy < 0:
                    tLy = 0

            if bRx < maxX:
                bRx += expandAmount
                if bRx > maxX:
                    bRx = maxX
            if bRy < maxY:
                bRy += expandAmount
                if bRy > maxY:
                    bRy = maxY

            return tLx,tLy,bRx,bRy

        tLX,tLY = 400,400
        bRX, bRY = 500,500
        sizeX = bRX - tLX
        sizeY = bRY - tLY
        screenShotRegion = (tLX,tLY,sizeX,sizeY)

        while True:
            try:
                matchingPixels = self.findColorsFast(colorToFind,screenShotRegion)
                y,x = matchingPixels[0]
                print("from find colors iteratively:", tLX + x, tLY + y)
                return tLX + x , tLY +y
            except IndexError:
                logger.debug("color not found attempting to expand screenshot area")

            try:
                tLX,tLY,bRX,bRY = expandImageRegion(tLX,tLY,bRX,bRY)
                sizeX = bRX - tLX
                sizeY = bRY - tLY
                screenShotRegion = (tLX,tLY,sizeX,sizeY)
            except TypeError:
                # print("findColorsIteratively - color not found")
                logger.debug("findColorsIteratively - color not found")
                raise TypeError
        
    def randomClickDurStdDiv(self):
        return round(recursiveTruncateRandGauss(0.08, 0.01, 0.13, 0.03),4)
    
    def randomTimeBetweenClicks(self):
        #too high of vaaleus possibly
        return round(recursiveTruncateRandGauss(0.175,0.015,0.4,0.100),4)

    def mouseClick(self, x:int, y:int, but:str = 'left'):
        # logger.debug("CLICKING")
        # print("CLICKING")
        dur = self.randomClickDurStdDiv()
        pyautogui.click(x,y,duration=dur,button=but)
        time.sleep(self.randomClickDurStdDiv())

    def multipeClicks(self,x, y):
        clickAmounts = round(recursiveTruncateRandGauss(2,1.10,6,.50))
        dur = self.randomClickDurStdDiv()
        print(f"Clicking {clickAmounts} times")
        for i in range(clickAmounts):
            # print("clicking")
            pyautogui.click(x=x,y=y,duration=self.randomClickDurStdDiv())
            # x,y = self.addVariance(x,y,random.randint(2,3))
            time.sleep(self.randomClickDurStdDiv())

    def rotateCameraWithMouse(self, direction, duration=0.4):
        """
        TODO:
        Update this method to instead use the api to read the pitch and yaw of camera to determine the appropriate angles
        ----------------------
        directions correspond to how the mouse moves not the camera necessarily
        this method could produce index errors be mindful
        """
        currentX, currentY =  pyautogui.position()

        directionsSimpleDict = {
            "up": -1,
            "down": 1,
            "left": -1,
            "right": 1
        }

        distance = 100 * (duration *  10) 
        #logging.debug("MOUSEFUNCTIONS:ROTATECAMERAWITHMOUSE: Rotating Camera...")
        if direction == "up" or  direction == "down":
            distanceTraveling = currentY + (distance * directionsSimpleDict[direction]) 
            pyautogui.dragTo(currentX, distanceTraveling, duration, button="middle")
        elif direction == "left" or direction == "right":
            distanceTraveling = currentX + (distance * directionsSimpleDict[direction]) 
            pyautogui.dragTo(distanceTraveling, currentY, duration, button="middle")
        elif direction == "upLeft":
            distanceX = -50 * (duration * 10)
            distanceY = -50 * (duration * 10)
            disTravelX = currentX + distanceX
            disTravelY = currentY + distanceY
            pyautogui.dragTo(disTravelX, disTravelY, duration, button="middle")
        elif direction == "upRight":
            distanceX = 50 * (duration * 10)
            distanceY = -50 * (duration * 10)
            disTravelX = currentX + distanceX
            disTravelY = currentY + distanceY
            pyautogui.dragTo(disTravelX, disTravelY, duration, button="middle")
        elif direction == "downLeft":
            distanceX = -50 * (duration * 10)
            distanceY = 50 * (duration * 10)
            disTravelX = currentX + distanceX
            disTravelY = currentY + distanceY
            pyautogui.dragTo(disTravelX, disTravelY, duration, button="middle")
        elif direction == "downRight":
            distanceX = 50 * (duration * 10)
            distanceY = 50 * (duration * 10)
            disTravelX = currentX + distanceX
            disTravelY = currentY + distanceY
            pyautogui.dragTo(disTravelX, disTravelY, duration, button="middle")

        self.moveMouseToArea(currentX,currentY,duration,areaVariance=10)

    def rotateCameraInRandomDirection(self, weightedDirection = None, weightAmount = 4 , dur = 0.4):
        #base total weight is eight careful on adding more weight to desired amount
        directionWeights = {
            "up":1,
            "down":1,
            "left":1,
            "right":1,
            "upLeft":1,
            "upRight":1,
            "downLeft":1,
            "downRight":1,
        }
        
        if weightedDirection != None:
            directionWeights[weightedDirection] = weightAmount
        
        weightsSum = sum(directionWeights.values())

        roll = random.randint(1, weightsSum)
        for item, weight in directionWeights.items():
            if roll <= weight:
                winningRoll = item
                break
            roll -= weight

        self.rotateCameraWithMouse(winningRoll, duration=dur)

    def mapAreaFinderAndClicker(self,img, conf:float = 0.75 , running:bool=False):
        #finds img using pyautogui and clicks on area
        w = 886
        h = 191
        attempts = 0
        maxAttempts = 4
        while attempts < maxAttempts:
            try:
                x, y = self.findImageSimple(img, w, h, conf)
                attempts = maxAttempts
            except ImageNotFoundException:
                attempts += 1
                #logging.exception("MOUSEFUNCTIONS:MAPAREAFINDERANDCLICKER: ImageNotFound Error")
                print("MOUSEFUNCTIONS:MAPAREAFINDERANDCLICKER: ImageNotFound Error")
            
        x, y = self.moveMouseToArea(x,y,duration=random.uniform(0.4,0.7),areaVariance=3)
        self.mouseClick(x,y)

def main():
    m = Mouse()

    # time.sleep(2)
    # # x,y = m.findImageIteratively("img/ffrightclicktext.png")
    # x,y = m.findImageSimple("img/ffrightclicktext.png")
    # print(x,y)

    # rDur = recursiveTruncateRandGauss(0.45,0.1,0.8,0.250)
    # print(rDur)
    rDur = 0.6
    # m.moveMouseToArea(1,1,duration=rDur,areaVariance=3,click=True)
    # m.moveMouseToArea(50,50,bezier=True)

    # result = m.findColorsRandomly((255,255,255),(1050,800,100,100))
    x,y = m.findColorsIteratively((0,255,255))
    print(x,y)

if __name__ == "__main__":
    main()
