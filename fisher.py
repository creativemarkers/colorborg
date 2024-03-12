import time
import pyautogui
import threading
from gui import Gui
from inventFunctions import Inventory
from mouseFunctions import Mouse
from verification import Verifyer
from camera import Camera
from pyautogui import ImageNotFoundException



class Fisher:

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
    

    FISHTYPE = [None,"shrimp","lobster","swordfish"]

    def __init__(self):

        self.main()


    def main(self):
        # gui for script selection
        # self.gui.getDesiredScript(self.FISHTYPE)
        # self.selectedSubScript = self.gui.scriptSelected
       
    
        self.botThread = threading.Thread(target = self.createBot, args=("shrimp",))
        self.botThread.start()
        self.infoGUI.displayBotInfo("Shrimp PowerFisher")
        self.infoGuiThread = threading.Thread(target = self.infoGUI.root.mainloop())
        self.infoGuiThread.start()
        
        

        
        
        # self.shrimp()

    def createThreads(self):
        pass

    def createBot(self,fishType):
        if fishType == "shrimp":
            shrimper = ShrimpFisher()
        
    def fish(self, fishSpotImageLocation):
        #confirm in fishing area
        #if not move to fishing area
        #find find fishing spot

        #enters loop after checking if inventory is full and if it's not currently fishing
        while self.invent.isInventFull(28) == False and self.verifyFishing() == False:
            
        
            #finds a potential fishing spot and gets it's coordinates
            potenialFishingSpotX, potenialFishingSpotY = self.findFishingSpot(fishSpotImageLocation)

            #moves mouse to to poential fishing spot, to verify with the text that pops up when hovering
            #over the fishing spot
            self.mouse.moveMouseToArea(potenialFishingSpotX,potenialFishingSpotY,1,5)

            #grabs pop up text
            textToCheck = self.verifyer.getText(8,32,120,20)

            #checks if the text matches the string
            if self.verifyer.verifyText(textToCheck,"Net Fishing Spot") == True:

                #sleep to make sure game is caught up
                time.sleep(0.1)
                #clicks on fishing spot
                pyautogui.click(potenialFishingSpotX,potenialFishingSpotY,duration=0.1,button='left')
                #sleep to make sure game is caught up
                time.sleep(10)

    def findFishingSpot(self, fishSpotImageLocation):
        #finds fishing spots and verifies it
        maxAttempts = 10
        attempt = 0
        maxTurnAttempt = 3
        turnAttempt = 0
        conf = 0.9

        while turnAttempt < maxTurnAttempt:
            while attempt < maxAttempts:
                try:

                    x , y = self.mouse.findImageSimple(fishSpotImageLocation, desiredConfidence = conf)

                    return x, y
                except ImageNotFoundException:
                    attempt += 1
                    print("image not found, attempt:", attempt)

            conf -= 0.1
            attempt = 0
            turnAttempt += 1
            
    
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
                    
                    time.sleep(0.6)

                self.invent.powerDropInventory(doNotDrop=1)
        
        else:
            print("powerFishing set to False")