#dependencies
import time
import pyautogui
import threading
import random
import logging
import sys
from gui import Gui
from infoGUI import InfoGUI
from inventFunctions import Inventory
from mouseFunctions import Mouse
from verification import Verifyer
from camera import Camera
from pyautogui import ImageNotFoundException
from universalMethods import Uni
from runeliteAPI import RuneLiteApi
from randomEventHandler import RandomEventHandler

pyautogui.MINIMUM_DURATION = 0.05

logger = logging.getLogger(__name__)

class Fisher:
    gui = Gui()
    infoGUI = InfoGUI()
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
    skillFishIconCords = (853,632)
    randomEventHandler = RandomEventHandler(mouse)

    api = RuneLiteApi()

    #array of fish currently supported (not really more for gui testing atm)
    FISHTYPE = ["shrimp","f2p fly fishing"]
    logger.info("successfully created fisher class variables")

    def __init__(self):
        self.main()
        self.running = True

    def main(self):

        # gui for script selection
        self.gui.getDesiredScript(self.FISHTYPE)
        self.selectedSubScript = self.gui.scriptSelected
        logger.info(f"{self.selectedSubScript} SELECTED")

        if self.gui.breaks == True:
            self.infoGUI.breaks = True

        self.botThread = threading.Thread(target = self.createBot, args=(self.gui.scriptSelected,))
        self.botThread.start()
        logger.info("CREATED thread for the bot")

        self.infoGuiThread = threading.Thread(target = self.infoGUI.main(self.gui.scriptSelected))
        self.infoGuiThread.start()
        logger.info("CREATED thread for GUI")

    def createBot(self,fishType):
        #creates bot instances, needed for threading
        logger.info(f"creating fish sub class object, {fishType}")
        if fishType == "shrimp":
            logger.info("shrimp fisher Chosen")
            shrimper = ShrimpFisher()
        elif fishType == "f2p fly fishing":
            logger.info("F2P fly fisher chosen")
            flyFisher = FlyFisher()

    def verifyGUIRunning(self):
        if self.infoGUI.isRunning == False:
            logger.critical("GUI was closed changed self.running to False, and exiting")
            #print("GUI Closed, exiting")
            self.uni.logOuter()
            self.running = False
            sys.exit()
        
    def fishWithImg(self, fishSpotImageLocation:str, rightClickImageLocation:str,
                    fishSpotVerificationString:str, stringVerificationRegion:tuple, 
                    animationID:int,):

        left,top,width,height = stringVerificationRegion
        
        logger.info("veryifing if able to fish")
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

                self.mouse.moveMouseToArea(potenialFishingSpotX,potenialFishingSpotY,areaVariance=5,bezier=True)

                #sleep for the game to catch up to the mouse moving
                time.sleep(round(random.uniform(0.15,0.25),4))

                textToCheck = self.verifyer.getText(left, top, width, height)

                self.infoGUI.scriptStatus = "Verifying fishing spot"
                if self.verifyer.verifyText(textToCheck, fishSpotVerificationString) == True:
                    #sleep to make sure game is caught up
                    time.sleep(0.1)
                    logger.info("clicking on fishing spot")
                    self.mouse.multipeClicks(potenialFishingSpotX,potenialFishingSpotY)
                    self.infoGUI.scriptStatus = "Moving to fishing spot"
                    
                    logger.info("waiting to walk/run to fishing spot")
                    time.sleep(1.2)
                    while not self.verifyFishing(animationID):
           
                        self.uni.waitTillIdle(self.api)

                        time.sleep(1.2)
                        moveStatus = self.api.getMovementStatus()
                        if moveStatus == "idle" and not self.verifyFishing(animationID):
                            print("didn't find fishing spot, looking for new fishing spot")
                            verified = False
                            break
                    verified = True
                    print("fishing")
                    self.infoGUI.scriptStatus = "Fishing"
                else:
                    logger.info("text didn't verify, right clicking spot")
                    if self.verifyer.rightClickVerifier(potenialFishingSpotX,potenialFishingSpotY,rightClickImageLocation):

                        time.sleep(1.2)
                        while not self.verifyFishing(animationID):
                            self.uni.waitTillIdle(self.api)
                            time.sleep(1.2)
                            moveStatus = self.api.getMovementStatus()
                            if moveStatus == "idle" and not self.verifyFishing(animationID):
                                print("didn't find fishing spot, looking for new fishing spot")
                                verified = False
                                break
                                
                            verified = True
                            print("fishing")
                            self.infoGUI.scriptStatus = "Fishing"
                    else:
                        verificationAttempts += 1
                        

            
        chanceToTurn = 1000
        self.cam.humanCameraBehavior(chanceToTurn)

        #random.randint(420,700)
        #^ideal way if it just checked every time on gather a fish
        if self.uni.statCheckDecider(2000,self.skillFishIconCords):
            print("checking stats from parent fish class")
            logger.info("Checked stats from fishWithImg")

    def findFishingSpot(self, fishSpotImageLocation):
        maxTurnAttempt = 4
        turnAttempt = 0

        logger.info("looking for fishing spot")

        while turnAttempt < maxTurnAttempt:
            try:
                x,y = self.mouse.findImageIteratively(fishSpotImageLocation,floorConfidence=0.4)
                return x,y
            except ImageNotFoundException:
                debugString = f"image not found, attempt: {turnAttempt}"
                print(debugString)
                logger.debug(debugString)

            self.mouse.moveMouseToArea(450,450,duration=random.uniform(0.4,0.7),areaVariance=40)
            self.mouse.rotateCameraInRandomDirection("downRight",dur=random.uniform(0.4,0.6))
        
            turnAttempt += 1
            
    def verifyFishing(self, animationID):
        
        result = self.api.getAnimation()

        if result == animationID:
            logger.debug("currently fishing")
            return True
        else:
            logger.info("not currently fishing")
            return False
        
    def hasBait(self, baitID):
        
        self.api.getInventoryData()
        inventArray = self.api.inventArray
        if any(slot["id"] == baitID for slot in inventArray):
            return True
        else:
            logger.critical("Attempting to logout due to lack of bait")
            self.uni.logOuter()
            self.running == False
            self.gui.fatalErrorPopUp("Ran out of bait, exiting...")
            sys.exit()

    def pauser(self):
        self.infoGUI.scriptStatus = "Script Paused"
        while self.infoGUI.pause:
            time.sleep(0.6)

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

    def shouldFishingLoopRun(self):

        if not self.infoGUI.isRunning:
            return False
        if self.infoGUI.takeBreak:
            return False
        if self.infoGUI.pause:
            return False
        if self.invent.isInventFull(28):
            return False
        return True

    def shrimp(self):
        time.sleep(0.5)

        if self.powerFish == True:
            #semi dead conditional, here as pseudo code, will be useful when banking is implemented

            while not self.uni.loggedinChecker():
                self.uni.loginOrchestrator()
            
            while self.infoGUI.isRunning:

                if self.infoGUI.pause:
                    self.pauser()
                  
                while self.shouldFishingLoopRun():
                    self.verifyGUIRunning()
                    self.randomEventHandler.randomEventHandler()
                    self.fishWithImg(self.shrimpSpotImg, self.fishingSpotVerificationString, self.verificationStringRegion, self.smallNetFishingAnimationID)
                    self.infoGUI.scriptStatus = "Fishing"
                    # self.uni.moveMouseOffScreen()
                    time.sleep(0.6)
                
                if self.infoGUI.isRunning and not self.infoGUI.pause:
                    if self.uni.statCheckDecider(abs(int(random.gauss(15,5))),self.skillFishIconCords):
                        logger.info("Checking stats from shrimper")
                    
                    if self.invent.inventFull and not self.infoGUI.pause:
                        self.infoGUI.scriptStatus = "Dropping inventory"
                        self.invent.betterPowerDropper(doNotDrop=1, amountToDrop=28)

            #this will more then likely need to be a universal function for reuse
                if self.infoGUI.takeBreak == True:
                    # print(f"taking break for {self.infoGUI.breakTime} seconds")
                    logger.info(f"takingn a break for: {self.infoGUI.breakTime} seconds")
                    formattedBreakTime = self.infoGUI.formatTime(self.infoGUI.breakTime)
                    self.infoGUI.scriptStatus = f"Taking a break for: {formattedBreakTime}"
                    time.sleep(random.uniform(0.6,1.2))
                    self.uni.logOuter()
                    time.sleep(self.infoGUI.breakTime)
                    self.uni.loginer()
                    self.infoGUI.takeBreak = False
                    self.infoGUI.lastBreak = time.time()
                    self.infoGUI.calculateTimes()
        else:
            pass

class FlyFisher(Fisher):

    flyFishingSpotImg = "img/salmonFishingIcon.png"
    ffRightClickImg = "img/ffrightclicktext.png"
    salmonColors = [(202,126,112),(174,95,81)]
    colorSearchRegion = (0, 0, 687, 726)
    flyfishingSpotVerificationString = "Lure Rod Fishing Spot"
    stringVerificationRegion = (8, 31, 152, 17)
    f2pLeftFishingBoundingCord = (3103,3424)
    f2pRightFishingBoundingCord = (3109,3433)
    ffAnimationID = 623
    bankBoothColor=(0,255,255)
    itemsID = [331,335]
    baitID = 314

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
        # guiStatus = self.infoGUI.scriptStatus
        self.powerFish = powerFishingSwitch
        self.flyFisherOrchestrator()

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
            self.uni.coordinateWalker(self.f2pRightFishingBoundingCord)
        else:
            self.uni.coordinateWalker(self.f2pLeftFishingBoundingCord)

    def shouldCoreLoopRun(self):
        if not self.infoGUI.isRunning:
            return False
        if self.infoGUI.pause:
            return False
        if self.infoGUI.takeBreak:
            return False
        if not self.hasBait(self.baitID):
            return False
        if self.invent.isInventFull(28):
            return False
        return True

    def flyFisherOrchestrator(self):

        def updateGuiStatus(status):
            self.infoGUI.scriptStatus = status

        while not self.uni.loggedinChecker():
                self.uni.loginOrchestrator()

        while self.infoGUI.isRunning == True:
            """
            TODO:
                add a popup when exiting
                want to add a verification if at fishing spot
                add fisher counter
                add xp an hour
            """

            if self.infoGUI.pause:
                    print("pausing")
                    self.pauser()

            updateGuiStatus("Checking Run Status")


            self.uni.runner(self.api)

            updateGuiStatus("Checking Inventory")

            while self.shouldCoreLoopRun():

                self.randomEventHandler.randomEventHandler()

                try:
                    self.fishWithImg(self.flyFishingSpotImg, self.ffRightClickImg, self.flyfishingSpotVerificationString, self.stringVerificationRegion, self.ffAnimationID)
                except TypeError:
                    logger.info("couldn't find fishing icon, changing fishing spots")
                    self.changef2pSpots()

                #self.uni.moveMouseOffScreen()
                
            if self.infoGUI.isRunning == True and not self.infoGUI.pause:
                if self.uni.statCheckDecider(abs(int(random.gauss(15,5))),self.skillFishIconCords):
                        logger.info("Checking stats from fly fisher")
                if self.invent.isInventFull(28):
                    updateGuiStatus("Dropping Inventory")
                    # itemsInInvent = self.invent.getAmountOfItemsInInvent(self.api)
                    self.invent.betterPowerDropper(doNotDrop=2, amountToDrop=28)

            if self.infoGUI.takeBreak == True:
                logger.info(f"takingn a break for: {self.infoGUI.breakTime} seconds")
                formattedBreakTime = self.infoGUI.formatTime(self.infoGUI.breakTime)
                self.infoGUI.scriptStatus = f"Taking a break for: {formattedBreakTime}"
                time.sleep(random.uniform(0.6,1.2))
                self.uni.logOuter()
                time.sleep(self.infoGUI.breakTime)
                self.uni.loginer()
                self.infoGUI.takeBreak = False
                self.infoGUI.lastBreak = time.time()
                self.infoGUI.calculateTimes()

def main():
    """
    for testing
    """
    pass

if __name__ == "__main__":
    main()