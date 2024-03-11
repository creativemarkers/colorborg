import pytesseract
from PIL import ImageGrab

class Verifyer:

    def __init__(self):
        pass

    def getText(self,left,top,width,height):
        #example usage: print(self.verifyer.getText(74,5,30,20)), if on vs code should return "edit"
        screenshot = ImageGrab.grab(bbox=(left,top,left+width, top+height))

        text = pytesseract.image_to_string(screenshot)

        cleanText = text.replace('\n','')

        return cleanText
    
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
            
            if len(cWords) < len(vWords):
                return False

            for i in range(len(vWords)):

                if cWords[i] == vWords[i]:
                    print("a word matched")
                    matches += 1
        
            if matches >= (len(vWords)/2):
                return True
            
            return False