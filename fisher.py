#dependencies
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

    #variables and objects required for the script to run
    #initialize gui mostly for parameter setting
    gui = Gui()
    #initialize infoGui
    infoGUI = Gui()
    #variable for infoGui thread
    infoGuiThread = None
    #variable for botThread
    botThread = None
    #creates an inventory object to call necessary functions
    invent = Inventory()
    #dead variable
    selectedSubScript = None
    #dead variable
    fishSpotImg = None
    #creates Mouse instance
    mouse = Mouse()
    #creates verifyer instance
    verifyer = Verifyer()
    #creates Camera instance, currently not being used but have plans too()
    cam = Camera()
    #dead variable
    currentlyFishing = False
    
    #array of fish currently supported (not really more for gui testing atm)
    FISHTYPE = [None,"shrimp","trout and salmon","lobster", "swordfish"]

    def __init__(self):
        #calls main when initialized
        self.main()


    def main(self):

        '''
        disabled gui prompts for ease of testing for now 3/12/2024
        '''
        # gui for script selection
        # self.gui.getDesiredScript(self.FISHTYPE)
        # self.selectedSubScript = self.gui.scriptSelected
       
        #creates thread for the bot and starts it, still need to pass the right arg
        self.botThread = threading.Thread(target = self.createBot, args=("shrimp",))
        self.botThread.start()
        #creates display gui, then creates thread and starts it
        self.infoGUI.displayBotInfo("Shrimp PowerFisher")
        self.infoGuiThread = threading.Thread(target = self.infoGUI.root.mainloop())
        self.infoGuiThread.start()
        
    def createThreads(self):
        #dead function created for brainstorming might use later to abstract code a bit more
        pass

    def createBot(self,fishType):
        #creates bot instances, needed for threading
        if fishType == "shrimp":
            shrimper = ShrimpFisher()
        
    def fish(self, fishSpotImageLocation):
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
        
class ShrimpFisher(Fisher):

    #variables required for the shrimp script
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
        #function responsible for fishing shrimp
        if self.powerFish == True:
            #semi dead conditional, here as pseudo code, will be useful when banking is implemented
            
            while True:
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

                #gets current inventory status
                self.invent.isInventFull(28)
                
                while not self.invent.inventFull:
                #loop runs until inventory full
                    
                    #calls fish function in parent class
                    self.fish(self.shrimpSpotImg)
                    
                    #this sleep might not be necessary anymore, as fish is now handling it
                    time.sleep(0.6)

                #calls invent obj to power drop the whole inventory minus the first slot (contains fishing net)
                self.invent.powerDropInventory(doNotDrop=1)
        
        else:
            print("powerFishing set to False")