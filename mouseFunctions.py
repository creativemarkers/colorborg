import pyautogui
import cv2
from time import sleep
import random


pyautogui.MINIMUM_DURATION = 0.05


def moveMouseToArea(x:int, y:int, duration=1, addAreaVariance = False, areaVariance:int = 0):

    xVaried, yVaried = addVariance(x, y, areaVariance)

    moveMouse(xVaried, yVaried, duration)

def moveMouse(x:int, y:int, duration=1):
      
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

def addVariance(x:int, y:int, varianceAmount:int):

    if varianceAmount <= 0:
        raise ValueError("Variance must be greater than 0")
       
    xCeilingVariance = x + varianceAmount
    xFloorVariance = x - varianceAmount

    yCeilingVariance = y + varianceAmount
    yFloorVariance = y - varianceAmount

    xVaried = random.range(xFloorVariance,xCeilingVariance)
    yVaried = random.range(yFloorVariance,yCeilingVariance)

    return xVaried, yVaried

def durationVariance(x, y, duration):

     
    currentX, currentY = pyautogui.position()

    # if x >= currentX and y >= currentY:
    #     distanceX = x - currentX
    #     distanceY = y - currentY
    #     totalDistance = (distanceX + distanceY) / 2
    # elif x <= currentX and y <= currentY:
    #     distanceX = currentX - x
    #     distanceY = currentY - y
    #     totalDistance = (distanceX + distanceY) / 2
    # elif x >= currentX and y <= currentY:
    #     distanceX = x - currentX
    #     distanceY = currentY - y
    #     totalDistance = (distanceX + distanceY) / 2
    # elif x <= currentX and y >= currentY:
    #     distanceX = currentX - x
    #     distanceY = y - currentY
    #     totalDistance = (distanceX + distanceY) / 2

    #can just use the abs() function

    distanceX = abs(x - currentX)
    distanceY = abs(y - currentY)

    totalDistance = (distanceX+distanceY)/2

    #controls the speed lowering the floor will make the duration slower
    calcedDuration = float(duration * (totalDistance/random.randrange(800,1700)))

    if calcedDuration < 0.05:
         return 0.05
    else:
        return calcedDuration
    
def findImageSimple(imageTofind:str, desiredConfidence = .999):
    
    # example call findImageSimple('img/test.png', .9)

    ss = pyautogui.screenshot(region=(0,0, 892, 892))

    imageLocation = pyautogui.locateOnScreen(imageTofind, region=(0,0, 892,892), confidence=desiredConfidence)
    #imageLocationCenter = pyautogui.center(imageLocation)
    x , y = pyautogui.center(imageLocation)
    # x, y = imageLocationCenter

    print("FROM MOUSE FUNCTIONS, found center of image:",x, y)

    return x , y

# def readTextFromImage():
     