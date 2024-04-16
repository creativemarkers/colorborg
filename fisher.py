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
from universalMethods import Uni
from runeliteAPI import RuneLiteApi



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
    uni = Uni()
    api = RuneLiteApi()

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
        
    def fishWithImg(self, fishSpotImageLocation:str, fishSpotVerificationString:str, stringVerificationRegion:tuple, animationID:int):
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
        while self.invent.isInventFull(28) == False and self.verifyFishing(animationID) == False:

            self.infoGUI.scriptStatus = "Looking for fishing spot"
            #finds a potential fishing spot and gets it's coordinates
            potenialFishingSpotX, potenialFishingSpotY = self.findFishingSpot(fishSpotImageLocation)

            #moves mouse to to poential fishing spot, to verify with the text that pops up when hovering
            #over the fishing spot
            durForFishSpot = random.uniform(0.5,1.0)
            self.mouse.moveMouseToArea(potenialFishingSpotX,potenialFishingSpotY,durForFishSpot,5)

            #grabs pop up text
            #print(stringVerificationRegion)
            textToCheck = self.verifyer.getText(left, top, width, height)
            self.infoGUI.scriptStatus = "Verifying fishing spot"

            #checks if the text matches the string
            verificationAttempts = 0
            maxVerifAttempts = 2
            verified = False
            while verified == False:
                if verificationAttempts > maxVerifAttempts:
                    self.mouse.rotateCameraInRandomDirection("downRight")

                if self.verifyer.verifyText(textToCheck, fishSpotVerificationString) == True:
                    #sleep to make sure game is caught up
                    time.sleep(0.1)
                    self.infoGUI.scriptStatus = "Moving to fishing spot"
                    pyautogui.click(potenialFishingSpotX,potenialFishingSpotY,duration=0.1,button='left')
                    startTime = time.time()
                    while not self.verifyFishing(animationID):
                        time.sleep(1)
                        elapsedTime = time.time() - startTime
                        if elapsedTime >= 10:
                            break
                    verified = True
                else:
                    verificationAttempts += 1
            
        #checks if camera should turn, the number below, to calculate chance = 1/n, n being the chanceToTurn variable
        chanceToTurn = 1000
        self.cam.humanCameraBehavior(chanceToTurn)

    def findFishingSpot(self, fishSpotImageLocation):
        #finds fishing spots and verifies it

        maxAttempts = 10
        attempt = 0
        maxTurnAttempt = 4
        turnAttempt = 0
        conf = 0.8

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
            self.mouse.rotateCameraInRandomDirection()
            #resets second loop, and lowers confidence variable
            conf -= 0.1
            attempt = 0
            turnAttempt += 1
            
    def verifyFishing(self, animationID):
        
        # text = self.verifyer.getText(54,55,44,20)
        
        # #print for debugging
        # print("Text captured to verify if fishing: %s" %text)

        result = self.api.getAnimation()

        if result == animationID:
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
    f2pLeftFishingBoundingCord = (3103,3424)
    f2pRightFishingBoundingCord = (3109,3433)
    ffAnimationID = 623
    bankBoothColor=(0,255,255)
    itemsID = [331,335]
    rightF2PfishingSpotToBankCords = [
        (3097,3442),
        (3090,3454),
        (3093,3456),
        (3098,3473),
        (3092,3490)
    ]
    leftF2PfishingSpotToBankCords = [
        (3091,3428),
        (3091,3445),
        (3088,3460),
        (3088,3466),
        (3100,3481),
        (3096,3485)
    ]
    f2pFromBankCords = [
        (3094,3486),
        (3099,3481),
        (3099,3476),
        (3088,3458),
        (3090,3446),
        (3090,3435),
        (3095,3435),
        (3100,3435),
        (3104,3431)
    ]

    def __init__(self, powerFishingSwitch:bool = True):
        self.powerFish = powerFishingSwitch
        self.flyFisher()

    def f2pFFspotChecker(self)->str:
        if self.verifyer.verifyInArea(self.api,self.f2pLeftFishingBoundingCord, 2):
            return "leftSpot"
        if self.verifyer.verifyInArea(self.api,self.f2pRightFishingBoundingCord, 3):
            return "rightSpot"
        
    def ffCordBanker(self):
        spot = self.f2pFFspotChecker()
        if spot == "leftSpot":
            self.uni.walkerCordinator(self.leftF2PfishingSpotToBankCords)
        else:
            self.uni.walkerCordinator(self.rightF2PfishingSpotToBankCords)
        self.uni.boothBanker(self.bankBoothColor,self.itemsID,self.api)
        self.uni.walkerCordinator(self.f2pFromBankCords)

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
            
            self.fishWithImg(self.flyFishingSpotImg, self.flyfishingSpotVerificationString, self.stringVerificationRegion, self.ffAnimationID)
            self.ffCordBanker()
        

def main():
    time.sleep(2)
    ff = FlyFisher()
    

if __name__ == "__main__":
    main()