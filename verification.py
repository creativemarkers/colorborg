import pytesseract
#import easyocr
from PIL import ImageGrab
import numpy as np
import logging
from mouseFunctions import Mouse

logger = logging.getLogger(__name__)

class Verifyer:

    totalDistanceFromTarget = None
    # reader = easyocr.Reader(['en'])

    def __init__(self):
        self.mouse = Mouse()
        #for right clicking
        pass

    def getText(self,left,top,width,height):
        #example usage: print(self.verifyer.getText(74,5,30,20)), if on vs code should return "edit"
        screenshot = ImageGrab.grab(bbox=(left,top,left+width, top+height))
        text = pytesseract.image_to_string(screenshot)
        cleanText = text.replace('\n','')
        return cleanText
    
    """
    below method is never used in my program
    """
    # def getTextEasyOCR(self,left,top,width,height):
    #     screenshot = ImageGrab.grab(bbox=(left,top,left+width, top+height))
    #     reader = easyocr.Reader(['en'])
    #     screenshot.save("screenshot.png")
    #     result = reader.readtext("screenshot.png")
    #     return result
    
    def verifyText(self,cleanedText, stringToVerify):

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
            
    # def getTextEnhanced(self,left,top,width,height, threshHold = False, targetColor = (0,0,0)):
    #     #can still try resizeing with easyocr as havent done that
        
    #     screenshot = ImageGrab.grab(bbox=(left,top,left+width, top+height))
    #     # resizedSS = screenshot.resize((width*20,height*20))
    #     screenshot_np = np.array(screenshot)

    #     result = self.reader.readtext(screenshot_np)

    #     for detection in result:
    #         print(detection[1])
       
    #     # resizedSS.save('img/tesseractTestImg.jpg')
    #     #enhanced_img.save('img/tesseractTestImg.jpg')
    #     # text = pytesseract.image_to_string(res)

    #     # cleanText = text.replace('\n','')

    #     return None

def main():
    pass

if __name__ == "__main__":
    main()