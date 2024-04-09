#dependencies
import time
import pyautogui
import threading
import random
from gui import Gui
from inventFunctions import Inventory
from mouseFunctions import Mouse
from verification import Verifyer
from camera import Camera
from pyautogui import ImageNotFoundException
from osFunctions import countFiles



class Fisher:

    #variables and objects required for the script to run
    gui = Gui()
    infoGUI = Gui()
    infoGuiThread = None
    botThread = None
    invent = Inventory()
    selectedSubScript = None
    fishSpotImg = None
    mouse = Mouse()
    verifyer = Verifyer()
    cam = Camera()
    currentlyFishing = False
    startTime = gui.startTime
    running = True

    #array of fish currently supported (not really more for gui testing atm)
    FISHTYPE = [None,"shrimp","trout and salmon","lobster", "swordfish"]

    def __init__(self):
        #calls main when initialized
        self.main()
        self.running = True

    def main(self):

        '''
        disabled gui prompts for ease of testing for now 3/12/2024
        '''
        # gui for script selection
        # self.gui.getDesiredScript(self.FISHTYPE)
        # self.selectedSubScript = self.gui.scriptSelected

        #creates thread for the bot and starts it, still need to pass the right arg
        self.botThread = threading.Thread(target = self.createBot, args=("salmon/trout",))
        self.botThread.start()

        #creates display gui, then creates thread and starts it
        # self.infoGUI.displayBotInfo("Shrimp PowerFisher")
        # self.infoGuiThread = threading.Thread(target = self.infoGUI.root.mainloop())
        # self.infoGuiThread.start()
       


        
    def createThreads(self):
        #dead function created for brainstorming might use later to abstract code a bit more
        pass

    def createBot(self,fishType):
        #creates bot instances, needed for threading
        if fishType == "shrimp":
            shrimper = ShrimpFisher()
        elif fishType == "salmon/trout":
            flyFisher = FlyFisher()

    def verifyRunning(self):

        if self.infoGUI.isRunning == False:
            print("GUI Closed, exiting")
            self.running = False
            exit()
        
    def fishWithImg(self, fishSpotImageLocation:str, fishSpotVerificationString:str, stringVerificationRegion:tuple):
        #main function that handles fishing
        #takes img of what the fishspot looks like

        '''
        pseudo code starts
        '''
        #confirm in fishing area
        #if not move to fishing area
        #find find fishing spot
        '''
        pseudo code ends
        '''
        left,top,width,height = stringVerificationRegion
        #enters loop after checking if inventory is full and if it's not currently fishing
        while self.invent.isInventFull(28) == False and self.verifyFishing() == False:

            self.infoGUI.scriptStatus = "Looking for fishing spot"
            #finds a potential fishing spot and gets it's coordinates
            potenialFishingSpotX, potenialFishingSpotY = self.findFishingSpot(fishSpotImageLocation)

            #moves mouse to to poential fishing spot, to verify with the text that pops up when hovering
            #over the fishing spot
            durForFishSpot = random.uniform(0.5,1.0)
            self.mouse.moveMouseToArea(potenialFishingSpotX,potenialFishingSpotY,durForFishSpot,5)

            #grabs pop up text
            print(stringVerificationRegion)

            textToCheck = self.verifyer.getText(left, top, width, height)

            self.infoGUI.scriptStatus = "Verifying fishing spot"
            #checks if the text matches the string
            if self.verifyer.verifyText(textToCheck, fishSpotVerificationString) == True:

                #sleep to make sure game is caught up
                time.sleep(0.1)
                #clicks on fishing spot
                self.infoGUI.scriptStatus = "Moving to fishing spot"
                pyautogui.click(potenialFishingSpotX,potenialFishingSpotY,duration=0.1,button='left')
                
                #sleep to make sure game is caught up
                time.sleep(5)
        
        #checks if camera should turn, the number below, to calculate chance = 1/n, n being the chanceToTurn variable
        chanceToTurn = 1000
        self.cam.humanCameraBehavior(chanceToTurn)

    def findFishingSpot(self, fishSpotImageLocation):
        #finds fishing spots and verifies it

        maxAttempts = 10
        attempt = 0
        maxTurnAttempt = 3
        turnAttempt = 0
        conf = 0.9

        #uses two while loops to get coordinates of fishing spots
        #first loop lowers confidence accuracy if
        while turnAttempt < maxTurnAttempt:

            #second loop simply trys until max attempts reached
            while attempt < maxAttempts:
                try:
                    x , y = self.mouse.findImageSimple(fishSpotImageLocation, desiredConfidence = conf)

                    return x, y
                except ImageNotFoundException:
                    attempt += 1
                    print("image not found, attempt:", attempt)

            #resets second loop, and lowers confidence variable
            conf -= 0.1
            attempt = 0
            turnAttempt += 1
            
    def verifyFishing(self):

    
        #verifies if currently fishing

        #calls verifyer object to retrieve text on top right of runelite plugin to determine if fishing
        #not redundacy needed seen tesseract OCR can read this part of the game with ease

        text = self.verifyer.getText(54,55,44,20)
        
        #print for debugging
        print("Text captured to verify if fishing: %s" %text)

        if text == "Fishing":
            return True
        else:
            return False

    def fishWithColor(self, fishIconColor):
        pass

    def findFishingSpotWithColor(self,fishIconColor:list, screenShotRegion:tuple):

        for color in fishIconColor:
            try:
                y,x = self.mouse.findColorsRandomly(color, screenShotRegion)
                return x, y
            except ImageNotFoundException:
                print("FISHER:FINDFISHINGSPOTWITHCOLOR: color not found trying other color")
        


class ShrimpFisher(Fisher):

    #variables required for the shrimp script
    inventoryCheckX = 730
    inventoryCheckY = 567
    colorToCheck = (178,152,139)
    slotsToFill = 27
    shrimpSpotImg = "img/shrimpFishingIcon.png"
    powerFish = True
    fishingSpotVerificationString = "Net Fishing Spot"
    verificationStringRegion = (8,32,120,20)

    def __init__(self,powerfishing=True):
        
        self.powerFish = powerfishing
        self.shrimp()

    def shrimp(self):
        time.sleep(0.5)
        #function responsible for fishing shrimp
        if self.powerFish == True:
            #semi dead conditional, here as pseudo code, will be useful when banking is implemented
            
            #while True:
            while self.running == True:
            #while self.infoGUI.isRunning == True:
            #horrible conditional but necessary for testing will more then likely need to changed to a quit command

                '''
                pseudo code starts
                '''
                #check for fishing net
                    #use pyautogui opencv to locate on invent
                #if fish net available check where in inventory it is
                #if not in first slot move it
                '''
                pseudo code ends
                '''
                self.verifyRunning()
                #gets current inventory status
                self.invent.isInventFull(28)
                
                while not self.invent.inventFull:
                #loop runs until inventory full
                    self.verifyRunning()
                    #calls fish function in parent class
                    self.fishWithImg(self.shrimpSpotImg, self.fishingSpotVerificationString, self.verificationStringRegion)
                    self.infoGUI.scriptStatus = "Fishing"
                    #this sleep might not be necessary anymore, as fish is now handling it
                    time.sleep(0.6)

                #calls invent obj to power drop the whole inventory minus the first slot (contains fishing net)
                self.infoGUI.scriptStatus = "Dropping inventory"
                self.invent.powerDropInventory(doNotDrop=1)
        
        else:
            print("powerFishing set to False")

class FlyFisher(Fisher):

    flyFishingSpotImg = "img/salmonFishingIcon.png"
    salmonColors = [(202,126,112),(174,95,81)]
    colorSearchRegion = (0, 0, 687, 726)
    flyfishingSpotVerificationString = "Lure Rod Fishing Spot"
    stringVerificationRegion = (8, 31, 152, 17)

    def __init__(self, powerFishingSwitch:bool = True):
        self.powerFish = powerFishingSwitch
        # self.flyFisher()

    def getSpot(self):
        pass

    def salmonBanker(self):
        pass
    
    def imgWalker(self, running=False):
        #current images are going to click on north part of the map assuming camera is pointing north
        leftSpotImgs = "img/salmonBankRunImgs/leftSpot"
        imgCount = countFiles(leftSpotImgs)
        for i in range(imgCount):
            imgPath = f"img/salmonBankRunImgs/leftSpot/{i+1}.png"
            self.mouse.mapAreaFinderAndClicker(imgPath)
            if running == True:
                time.sleep(8)
            else:
                time.sleep(15)

    def flyFisher(self):
        #orchestrates fishing functions
        """
        confirm fishing equipment is in inventory
        confirm in fishing spot
            okay can run
                run checker
                check inventory space
                    if invent full
                        bank or drop
                            if bank 
                                break out of inner loop and start banking
                            elif drop
                                quick drop invent
                    find fishing spot
                    verify fishing spot
                    click on fishing spot
                    wait to stop fishing
                    go to run checker
        """

        while True:
            # x, y = self.findFishingSpotWithColor(self.salmonColors, self.colorSearchRegion)
            # print(x, y)
            self.fishWithImg(self.flyFishingSpotImg, self.flyfishingSpotVerificationString, self.stringVerificationRegion)

def main():
    time.sleep(3)
    ff = FlyFisher()
    ff.salmonBanker()

if __name__ == "__main__":
    main()