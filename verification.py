import pytesseract
import easyocr
from PIL import ImageGrab
import numpy as np



class Verifyer:

    reader = easyocr.Reader(['en'])

    def __init__(self):
        pass



    def getText(self,left,top,width,height):
        #example usage: print(self.verifyer.getText(74,5,30,20)), if on vs code should return "edit"
        screenshot = ImageGrab.grab(bbox=(left,top,left+width, top+height))

        text = pytesseract.image_to_string(screenshot)

        cleanText = text.replace('\n','')

        return cleanText
    

    def getTextEnhanced(self,left,top,width,height, threshHold = False, targetColor = (0,0,0)):
        #can still try resizeing with easyocr as havent done that
        
        screenshot = ImageGrab.grab(bbox=(left,top,left+width, top+height))
        # resizedSS = screenshot.resize((width*20,height*20))
        screenshot_np = np.array(screenshot)

        result = self.reader.readtext(screenshot_np)

        for detection in result:
            print(detection[1])
       


            

        # resizedSS.save('img/tesseractTestImg.jpg')
        #enhanced_img.save('img/tesseractTestImg.jpg')
        # text = pytesseract.image_to_string(res)

        # cleanText = text.replace('\n','')

        return None
    
    def verifyText(self,cleanedText, stringToVerify):

        cleanedText.lower()
        stringToVerify.lower()
        matches = 0
        
        if cleanedText == stringToVerify:
            return True
        else:
            cWords = cleanedText.split()
            vWords = stringToVerify.split()
            print(cWords)
            print(vWords)
            
            # if len(cWords) < len(vWords):
            #     return False
            try:
                for i in range(len(vWords)):

                    if i <=  len(cWords) and cWords[i] == vWords[i]:
                        print("A word matched")
                        return True
            except IndexError:
                print("VERIFICATION:VERIFYTEXT: Index Error, returning False")
                return False
        
            # if matches >= 1:
            #     print("Words matched:", matches)
            #     return True
            
            return False