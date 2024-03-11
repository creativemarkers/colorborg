import time
import pyautogui
from gui import Gui
from inventFunctions import Inventory
from mouseFunctions import Mouse
from verification import Verifyer


class Fisher:

    gui = Gui()
    invent = Inventory()
    selectedSubScript = None
    fishSpotImg = None
    mouse = Mouse()
    verifyer = Verifyer()
    currentlyFishing = False

    FISHTYPE = [None,"shrimp","lobster","swordfish"]

    def __init__(self):

        self.main()


    def main(self):
        #gui for selection
        # self.gui.getDesiredScript(self.FISHTYPE)
        # self.selectedSubScript = self.gui.scriptSelected
        # print("in fisher main")


        #print(self.verifyer.getText(8,32,120,20))
        shrimper = ShrimpFisher()
        
        # self.shrimp()
        

    
    def fish(self, fishSpotImageLocation):
        #confirm in fishing area
        #if not move to fishing area
        #find find fishing spot
        falsePositiveCounter = 0

        while self.verifyFishing() == False:

            #currently not verifying if fishing spot

            potenialFishingSpotX, potenialFishingSpotY = self.findFishingSpot(fishSpotImageLocation)
            self.mouse.moveMouseToArea(potenialFishingSpotX,potenialFishingSpotY,1,5)
            time.sleep(0.1)
            pyautogui.click(potenialFishingSpotX,potenialFishingSpotY,duration=0.1,button='left')
            time.sleep(10)
            
                # textToCheck = self.verifyer.getText(8,32,120,20)
                # print(textToCheck)
                # if self.verifyer.verifyText(textToCheck,"Net Fishing spot") == True:
                #     print("Fishing spot Verified, clicking")
                #     time.sleep(0.2)
                #     pyautogui.click(potenialFishingSpotX,potenialFishingSpotY,duration=0.2,button='left')
                #     time.sleep(5)
                #     falsePositiveCounter = 0
                # else:
                #     falsePositiveCounter += 1

    
     
        # back to function that called to verify invent status


    def findFishingSpot(self, fishSpotImageLocation):
        #finds fishing spots and verifies it

        x , y = self.mouse.findImageSimple(fishSpotImageLocation, .9)

        return x,y
    
    def verifyFishing(self):
        text = self.verifyer.getText(54,55,44,20)
        print("Text captured to verify if fishing: %s" %text)
        if text == "Fishing":
            return True
        else:
            return False
        

class ShrimpFisher(Fisher):

    inventoryCheckX = 730
    inventoryCheckY = 567
    colorToCheck = (178,152,139)
    slotsToFill = 27
    shrimpSpotImg = "img/shrimpFishingIcon.png"
    powerFish = True

    def __init__(self,powerfishing=True):
        self.powerFish = powerfishing
        self.shrimp()

    def shrimp(self):
        #load info gui
        #log in check
        #check if logged in, if not log in or quit run
        if self.powerFish == True:

            while True:

                self.invent.isInventFull(28)

                #loop runs until invent full
                while not self.invent.inventFull:
                    self.fish(self.shrimpSpotImg)
                    self.invent.isInventFull(28)

                self.invent.powerDropInventory(doNotDrop=1)
        
        else:
            print("powerFishing set to False")