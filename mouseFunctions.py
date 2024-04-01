import pyautogui
import cv2
import time
import random
from pyautogui import ImageNotFoundException
import numpy


pyautogui.MINIMUM_DURATION = 0.05

class Mouse:

    def __init__(self):
        pyautogui.FAILSAFE = True

    #def moveMouseToArea(x:int, y:int, duration=1, addAreaVariance = False, areaVariance:int = 0):
    def moveMouseToArea(self, x:int, y:int, duration=1, areaVariance:int = 0, click:bool=False):
        xVaried = x
        yVaried =  y

        if areaVariance > 0:
            xVaried, yVaried = self.addVariance(x, y, areaVariance)

        self.moveMouse(xVaried, yVaried, duration)
    
        if click == True:
            self.mouseClick(xVaried,yVaried)

        if areaVariance > 0:
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

        if willTween >= 5:
            pyautogui.moveTo(x,y, duration, random.choice(tweeningList))
        else:
            duration /= 2
            pyautogui.moveTo(x, y, duration)

    def addVariance(self, x:int, y:int, varianceAmount:int):

        if varianceAmount <= 0:
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

            print("MOUSEFUNCTIONS:FINDIMAGESIMPLE: found center of image:",x, y)

            return x , y
        except ImageNotFoundException:
            raise ImageNotFoundException
        
    def findColorFast(self, colorToFind:tuple, desiredRegion:tuple):
        #note the elements in matching pixels are reversed so instead of getting x,y it gives us y,x
        #currently just looking at pixels left to right
        im = pyautogui.screenshot(region=desiredRegion)
        imArr = numpy.array(im)
        # colorToFind = numpy.array(colorToFind)
        matchingPixels = numpy.argwhere(numpy.all(imArr == colorToFind, axis=-1))
        return matchingPixels




    def mouseClick(self, x:int, y:int, but:str = 'left'):
        print("CLICKING")
        dur = random.uniform(0.01,0.1)
        pyautogui.click(x,y,duration=dur,button=but)
        clep = random.uniform(0.05,0.1)
        time.sleep(clep)


