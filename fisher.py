#dependencies
import time
import pyautogui
import threading
import random
import logging
from gui import Gui
from inventFunctions import Inventory
from mouseFunctions import Mouse
from verification import Verifyer
from camera import Camera
from pyautogui import ImageNotFoundException
from universalMethods import Uni
from runeliteAPI import RuneLiteApi
from logOrganizer import LogOrganizer

log = LogOrganizer(__name__)
log.setupDirectory()
logging.basicConfig(level=logging.DEBUG, filename="fisher_Log.log", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
    FISHTYPE = [None,"shrimp","f2p fly fishing"]
    logger.info("successfully created fisher class variables")

    def __init__(self):
        self.main()
        self.running = True

    def main(self):

        # gui for script selection
        self.gui.getDesiredScript(self.FISHTYPE)
        self.selectedSubScript = self.gui.scriptSelected
        logger.info("GOT Subscript")

        #creates thread for the bot and starts it, still need to pass the right arg
        
        self.botThread = threading.Thread(target = self.createBot, args=(self.gui.scriptSelected,))
        self.botThread.start()
        logger.info("CREATED thread for the bot")

        #creates display gui, then creates thread and starts it
    
        self.infoGUI.displayBotInfo("Shrimp PowerFisher")
        self.infoGuiThread = threading.Thread(target = self.infoGUI.root.mainloop())
        self.infoGuiThread.start()
        logger.info("CREATED thread for GUI")

    def createBot(self,fishType):
        #creates bot instances, needed for threading
        logger.info(f"creating fish sub class object, {fishType}")
        if fishType == "shrimp":
            shrimper = ShrimpFisher()
        elif fishType == "f2p fly fishing":
            flyFisher = FlyFisher()

    def verifyGUIRunning(self):
        if self.infoGUI.isRunning == False:
            logger.critical("GUI was closed changed self.running to False, and exiting")
            #print("GUI Closed, exiting")
            self.running = False
            exit()
        
    def fishWithImg(self, fishSpotImageLocation:str, fishSpotVerificationString:str, stringVerificationRegion:tuple, animationID:int):

        left,top,width,height = stringVerificationRegion

        while self.invent.isInventFull(28) == False and self.verifyFishing(animationID) == False:

            verificationAttempts = 0
            maxVerifAttempts = 2
            verified = False
            while verified == False:
                if verificationAttempts > maxVerifAttempts:
                    self.mouse.rotateCameraInRandomDirection("downRight")
                    verificationAttempts = 0

                self.infoGUI.scriptStatus = "Looking for fishing spot"
                
                potenialFishingSpotX, potenialFishingSpotY = self.findFishingSpot(fishSpotImageLocation)

                durForFishSpot = random.uniform(0.4,0.7)
                self.mouse.moveMouseToArea(potenialFishingSpotX,potenialFishingSpotY,durForFishSpot,5)

                #print(stringVerificationRegion)
                textToCheck = self.verifyer.getText(left, top, width, height)
                self.infoGUI.scriptStatus = "Verifying fishing spot"


                if self.verifyer.verifyText(textToCheck, fishSpotVerificationString) == True:
                    verified = True
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
                    self.infoGUI.scriptStatus = "Fishing"
                else:
                    verificationAttempts += 1
            
        chanceToTurn = 1000
        self.cam.humanCameraBehavior(chanceToTurn)

    def findFishingSpot(self, fishSpotImageLocation):
        maxAttempts = 10
        attempt = 0
        maxTurnAttempt = 4
        turnAttempt = 0
        conf = 0.8

        while turnAttempt < maxTurnAttempt:
        
            while attempt < maxAttempts:
                try:
                    x , y = self.mouse.findImageSimple(fishSpotImageLocation, desiredConfidence = conf)

                    return x, y
                except ImageNotFoundException:
                    attempt += 1
                    debugString = f"image not found, attempt: {attempt}"
                    print(debugString)
                    logger.debug(debugString)

            self.mouse.moveMouseToArea(450,450,duration=random.uniform(0.4,0.7),areaVariance=40)
            self.mouse.rotateCameraInRandomDirection("downRight",dur=random.uniform(0.4,0.6))
            
            conf -= 0.1
            attempt = 0
            turnAttempt += 1
            
    def verifyFishing(self, animationID):
        
        result = self.api.getAnimation()

        if result == animationID:
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
    fishingSpotVerificationString = "Net Fishing Spot"
    verificationStringRegion = (8,32,120,20)
    smallNetFishingAnimationID = 621

    def __init__(self,powerfishing=True):
        
        self.powerFish = powerfishing
        self.shrimp()

    def shrimp(self):
        time.sleep(0.5)

        if self.powerFish == True:
            #semi dead conditional, here as pseudo code, will be useful when banking is implemented
            
           
            while self.running == True:
            #while self.infoGUI.isRunning == True:
            #horrible conditional but necessary for testing will more then likely need to changed to a quit command

                self.verifyGUIRunning()

                self.invent.isInventFull(28)
                
                while not self.invent.inventFull:
                    self.verifyGUIRunning()
                    self.fishWithImg(self.shrimpSpotImg, self.fishingSpotVerificationString, self.verificationStringRegion, self.smallNetFishingAnimationID)
                    self.infoGUI.scriptStatus = "Fishing"
                    #this sleep might not be necessary anymore, as fish is now handling it
                    time.sleep(0.6)
                if self.infoGUI.isRunning == True:
                    self.infoGUI.scriptStatus = "Dropping inventory"
                    itemsInInvent = self.invent.getAmountOfItemsInInvent(self.api)
                    self.invent.powerDropInventory(doNotDrop=1, amountToDrop=itemsInInvent)
        
        else:
            #print("powerFishing set to False")
            pass

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
        guiStatus = self.infoGUI.scriptStatus
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

    def changef2pSpots(self)->None:
        spot = self.f2pFFspotChecker()
        if spot == "leftSpot":
            self.uni.walkerCordinator(self.f2pRightFishingBoundingCord)
        else:
            self.uni.walkerCordinator(self.f2pLeftFishingBoundingCord)

    #orchestrates fly fishing 
    def flyFisher(self):

        def updateGuiStatus(status):
            self.infoGUI.scriptStatus = status

        while self.infoGUI.isRunning == True:
            """
            TODO:
                want to add a verification if at fishing spot
                add fisher counter
                add xp an hour

            """
            updateGuiStatus("Checking Run Status")
            self.uni.runner(self.api)

            updateGuiStatus("Checking Inventory")
            while not self.invent.isInventFull(28) and self.infoGUI.isRunning == True:
                try:
                    self.fishWithImg(self.flyFishingSpotImg, self.flyfishingSpotVerificationString, self.stringVerificationRegion, self.ffAnimationID)
                except TypeError:
                    logger.info("couldn't find fishing icon, changing fishing spots")
                    self.changef2pSpots()

            if self.infoGUI.isRunning == True:
                updateGuiStatus("DroppingInventory")
                itemsInInvent = self.invent.getAmountOfItemsInInvent(self.api)
                self.invent.powerDropInventory(doNotDrop=2, amountToDrop=itemsInInvent)

def main():
    # time.sleep(2)
    # ff = FlyFisher()
    i = Inventory()
    api = RuneLiteApi()

    result = i.getAmountOfItemsInInvent(api)
    i.powerDropInventory(1,result)

if __name__ == "__main__":
    main()