import pyautogui
import cv2
import time
import random
from pyautogui import ImageNotFoundException
import numpy
import os
import logging


pyautogui.MINIMUM_DURATION = 0.05

logger = logging.getLogger(__name__)

class Mouse:

    def __init__(self):
        pyautogui.FAILSAFE = True

    def moveMouseToArea(self, x:int, y:int, duration=1, areaVariance:int = 0, click:bool=False):
        xVaried = x
        yVaried =  y

        if areaVariance > 0:
            xVaried, yVaried = self.addVariance(x, y, areaVariance)

        self.moveMouse(xVaried, yVaried, duration)
    
        if click == True:
            self.mouseClick(xVaried,yVaried)

        return xVaried, yVaried  
                         
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
            pyautogui.moveTo(x,y, duration, random.choice(tweeningList))
        else:
            duration /= 1.5
            pyautogui.moveTo(x, y, duration)

    def addVariance(self, x:int, y:int, varianceAmount:int):

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
    
    def findColorsIteratively(self):
        # TODO !!!
        #uses find colors randomly function
        #useful for searching near player 
        pass

    def findImgIteratively(self):
        # TODO !!!
        #useful for searching near player
        pass

    def mouseClick(self, x:int, y:int, but:str = 'left'):
        logger.debug("CLICKING")
        print("CLICKING")
        dur = random.uniform(0.01,0.1)
        pyautogui.click(x,y,duration=dur,button=but)
        clep = random.uniform(0.05,0.1)
        time.sleep(clep)

    def rotateCameraWithMouse(self, direction, duration=0.4):
        #directions correspond to how the mouse moves not the camera necessarily
        #this method could produce index errors be mindful

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

if __name__ == "__main__":
    pass