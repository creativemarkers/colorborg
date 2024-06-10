import pytesseract
#import easyocr
from PIL import ImageGrab
import numpy as np
import logging
from mouseFunctions import Mouse
from utils.fernsUtils import recursiveTruncateRandGauss
from pyautogui import ImageNotFoundException

logger = logging.getLogger(__name__)

def getText(left,top,width,height):
    #example usage: print(self.verifyer.getText(74,5,30,20)), if on vs code should return "edit"
    logger.info("grabbing text to read")
    screenshot = ImageGrab.grab(bbox=(left,top,left+width, top+height))
    text = pytesseract.image_to_string(screenshot)
    cleanText = text.replace('\n','')
    return cleanText


def verifyText(cleanedText, stringToVerify):
    logger.info("verifying text")
    cleanedText = cleanedText.lower()
    stringToVerify = stringToVerify.lower()

    if cleanedText == stringToVerify:
        return True
    
    logger.debug("grabbed text doesn't match, attempting to clean to further verify")
    cWords = cleanedText.split()
    vWords = stringToVerify.split()
    print(cWords)
    print(vWords)
    logger.debug(cWords)
    logger.debug(vWords)
    

    needToMatch = len(vWords) // 2
    matches = 0

    if needToMatch == 0:
        needToMatch = 1
    
    for word in vWords:
        if word in cWords:
            matches += 1
    
    if matches >= needToMatch:
        print("split words matches:", matches)
        return True
        
    print("no match")
    return False

class Verifyer:

    totalDistanceFromTarget = None
    # reader = easyocr.Reader(['en'])

    def __init__(self):
        self.mouse = Mouse()
        #for right clicking
        pass

    def getText(self,left,top,width,height):
        #example usage: print(self.verifyer.getText(74,5,30,20)), if on vs code should return "edit"
        logger.info("grabbing text to read")
        screenshot = ImageGrab.grab(bbox=(left,top,left+width, top+height))
        text = pytesseract.image_to_string(screenshot)
        cleanText = text.replace('\n','')
        return cleanText
    
    def verifyText(self,cleanedText, stringToVerify):
        logger.info("verifying text")
        cleanedText = cleanedText.lower()
        stringToVerify = stringToVerify.lower()

        if cleanedText == stringToVerify:
            return True
        
        logger.debug("grabbed text doesn't match, attempting to clean to further verify")
        cWords = cleanedText.split()
        vWords = stringToVerify.split()
        #prints below for debugging
        print(cWords)
        print(vWords)
        logger.debug(cWords)
        logger.debug(vWords)
        
        # cWordsDict = {}

        # for word in cWords:
        #     if word not in cWordsDict:
        #         cWordsDict[word] = 1
        #     else:
        #         cWordsDict[word] += 1

        needToMatch = len(vWords) // 2
        matches = 0

        if needToMatch == 0:
            needToMatch = 1
        
        for word in vWords:
            if word in cWords:
                matches += 1
        
        if matches >= needToMatch:
            print("split words matches:", matches)
            return True
           
        print("no match")
        return False
        
    def verifyInArea(self, api:object, boundingTile:tuple, MaxRange:int)-> bool:
        currentWorldPos = api.getCurrentWorldPosition()
        print(boundingTile)
        desiredX, desiredY =  boundingTile

        currentX,currentY = currentWorldPos

        distX = abs(currentX-desiredX)
        distY = abs(currentY-desiredY)
        # print(f"distX: {distX}")
        # print(f"distY: {distY}")
        
        if distX > 0 and distY > 0:
            self.totalDistanceFromTarget = (distX+distY)//2
        else:
            self.totalDistanceFromTarget = distX + distY

        if self.totalDistanceFromTarget > MaxRange:
            return False
        elif self.totalDistanceFromTarget > MaxRange:
            return False
        else:
            return True
        
    def rightClickVerifier(self,x,y,imgToFind):

        self.mouse.mouseClick(x,y,but='right')
        try:
            x,y = self.mouse.findImageSimple(imgToFind)
            rDur = recursiveTruncateRandGauss(0.45,0.1,0.8,0.250)
            self.mouse.moveMouseToArea(x,y,rDur,areaVariance=3,click=True)
            return True
        except ImageNotFoundException:
            return False

def main():

    import time

    m = Mouse()
    v = Verifyer()
    time.sleep(1)
    x,y = m.findImageIteratively("img/salmonFishingIcon.png")
    x,y = m.moveMouseToArea(x,y,duration=0.5,areaVariance=5)
    result = v.rightClickVerifier(x,y,"img/ffrightclicktext.png")
    print(result)

    pass

if __name__ == "__main__":
    main()