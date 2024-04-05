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
from runeliteAPI import RuneLiteApi


class Slayer:

    gui = Gui()
    infoGUI = Gui()
    infoGuiThread = None
    botThread = None
    invent = Inventory()
    selectedSubScript = None
    mouse = Mouse()
    verifyer = Verifyer()
    cam = Camera()
    startTime = gui.startTime
    nothingNearToPickup = None
    running = None
    monsterName = None
    monsterSlain = 0
    api = RuneLiteApi()
    item1InvPosition = None
    item1Quant = None

    MONSTERHIGHLIGHT = (0,255,255)

    def __init__(self):
        self.main()
        
    def main(self):
        
        #startThreads
        time.sleep(1)
        chickenSlayer = ChickenSlayer()
        #get which attack style to prio?

        # self.botThread = threading.Thread(target = self.createBot, args=("shrimp",))
        # self.botThread.start()
        # #creates display gui, then creates thread and starts it
        # self.infoGUI.displayBotInfo("Shrimp PowerFisher")
        # self.infoGuiThread = threading.Thread(target = self.infoGUI.root.mainloop())
        # self.infoGuiThread.start()
    
        #check if running(in game)

    def slay(self, monsterName:str, monsterHighlightColor:tuple) -> None:
        #make sure your monster is highlighted
        #while api npcname null

        monsterKilled = False
        monsterFindAttempt = 0
        maxMonsterFindAttempt = 3

        while self.getFightingStatus() == False or monsterKilled == False:

            if monsterFindAttempt > maxMonsterFindAttempt:
                rDur = random.uniform(0.52, 0.83)
                self.mouse.rotateCameraInRandomDirection(weightedDirection="downRight", dur=rDur)
                monsterFindAttempt -= 2

            x,y = self.findMonster(monsterHighlightColor)

            if self.veriyMonster(monsterName) == True:
                monsterFindAttempt = 0
                self.mouse.mouseClick(x,y)
                time.sleep(3)
                npcName, npcHealth = self.api.getNPCinfo()
                while npcHealth > 0:
                    time.sleep(0.5)
                    npcName, npcHealth = self.api.getNPCinfo()
                monsterKilled = True
            else:
                monsterFindAttempt += 1
                print("SLAYER:SLAY:MONSTER NOT FOUND")

        return None
    
    def getFightingStatus(self) -> bool:
        
        npcName, npcHealth = self.api.getNPCinfo()

        if npcName != "null" or npcHealth > 0:
            return True
        else:
            return False

    def veriyMonster(self, monsterName:str) -> bool:
        #assumes mouse is over chicken already
        text = self.verifyer.getText(10, 33, 105, 12)
        verifyingText = "Attack " + monsterName
        if self.verifyer.verifyText(text, verifyingText) == True:
            return True
        else:
            return False

    def findMonster(self,monsterHighlightColor:tuple) -> int:
        #finds monster, and moves mouse to get ready for verification
        #nature of npc it's possible adding variance to the mouse can set it out of bounds need to account for this.
        try:
            region = (0,0,688,726)
            matchingPixels = self.mouse.findColorsRandomly(monsterHighlightColor, region)
            # matchingPixels = self.mouse.findColorsFast(monsterHighlightColor, region)
            
            y,x = matchingPixels[0]
            # print(x, y)
            randDur = random.uniform(0.2,0.4)
            randArea = random.randint(1,4)
            #removing random area for now
            x,y = self.mouse.moveMouseToArea(x,y,randDur)
            return x,y
        except IndexError:
            raise IndexError
    
    def runner(self):
        #need a semi refact OCR engines are awful at reading small text like the run energy, will need to do
        #time based system for handling run, (takes 12 min to full run energy from 0)
        #runelite api
        #handles running
        runningColor = (206,168,1)
        x, y = 738, 160

        if pyautogui.pixelMatchesColor(x, y, runningColor) != True:
            print("SLAYER:RUNNER: Not running")
            runningThreshold = random.randint(50, 80)

            currentRunEnergy = self.api.getRunEnergy()

            print(currentRunEnergy)

            if currentRunEnergy >= runningThreshold:
                print("SLAYER:RUNNER: Clicking on run icon")
                dur = random.uniform(0.3,0.5)
                self.mouse.moveMouseToArea(735,165, duration=dur, areaVariance=10,click=True)
        else:
            print("SLAYER:RUNNER: Running")
            
    def pickUpNearbyDrops(self, dropImg, dropName, amountToPickUp):
        
        playerLocationX = 452
        playerLocationY = 468

        distanceThreshold = 200

        availableDrops = pyautogui.locateAllOnScreen('img/featherText.png',region=(0,0,900,900),confidence=0.6)

        dropsNeaby = []

        for drop in availableDrops:
            dropX,dropY = pyautogui.center(drop)
            absX = abs(playerLocationX - dropX)
            absY = abs(playerLocationY - dropY) 

    def pickUpDrop(self,dropName, dropImg, textVerificationPos, itemId):
        #need it to sample a random region of the screen the topright to bottom left makes it so obvious a bot
        #attempts to find drop, verifys if drop, clicks if it is.
        print("SLAYER:PICKUPDROP: Starting pick up drop method ...")
        if self.item1InvPosition == None:
            self.item1InvPosition, self.item1Quant = self.api.getItemQuantityComplete(itemId)

        # try:
        #     x, y = self.findDrops(dropImg)
        # except TypeError:
        #     print("SLAYER:PICKUPDROP:No drop found.")
        #     return None
        # x, y = self.mouse.moveMouseToArea(x, y, duration=(random.uniform(0.2,0.4)), areaVariance=1)
        # dropBool = self.verifyDropName(dropName, textVerificationPos)
        # print(dropBool)
        maxAttempts = 6
        attempts = 0
        lastX = 0
        lastY = 0
        ocrFail = 0
        ocrFailThreshold = 5

        while attempts < maxAttempts:

            try:
                x, y = self.findDrops(dropImg)
            except TypeError:
                print("SLAYER:PICKUPDROP:No drop found.")
                return None
            
            x, y = self.mouse.moveMouseToArea(x, y, duration=(random.uniform(0.2,0.4)), areaVariance=1)
            dropBool = self.verifyDropName(dropName, textVerificationPos)

            if dropBool == True:
                # currentWorldPos = self.api.getCurrentWorldPosition()
                print("SLAYER:PICKUPDROP: Attempting to Click on drop")
                self.mouse.mouseClick(x,y)
                #this sleep needs to be replaced with a method that checks if the feather was picked up
                result = self.waitForDropPickup()
                if result == True:
                    return True
                else:
                    attempts += 1
            else:
                if x == lastX and y == lastY:
                    attempts += 1
                    ocrFail += 1
                else:
                    ocrFail = 0
                    lastX = x
                    lastY = y
                    attempts += 1

        if ocrFail >= ocrFailThreshold:
            print("SLAYER:PICKUPDROP: Triggered OCR Fail.. Clicking")
            self.mouse.mouseClick(x,y)
            ocrFail = 0
            #this sleep needs to be replaced with a method that checks if the feather was picked up
            self.waitForDropPickup()


    
    def dropPickedUp(self):

        currentItem1Quanty = self.api.getItemQuantityInInventory(self.item1InvPosition)

        if currentItem1Quanty > self.item1Quant:
            self.item1Quant = currentItem1Quanty
            return True
        else:
            return False

    def waitForDropPickup(self):
        attempts = 0
        time.sleep(0.6)
        for _ in range(5):
                if self.dropPickedUp() == True:
                    return True
                else:
                    attempts += 1
                    time.sleep(0.6)
        return attempts
            
    def findDrops(self,dropImgLocation, conf:float = 0.6, multiple:bool = False):
        if multiple == False:
            try:
                x, y = self.mouse.findImageSimple(dropImgLocation,900,900,desiredConfidence = conf)
                return x, y
            except ImageNotFoundException:
                return print("single drop not found")
        else:
            try:
                dropAvailableDrops = pyautogui.locateAllOnScreen(dropImgLocation,region=(0,0,900,900),confidence= conf)
                return dropAvailableDrops
            except ImageNotFoundException:
                return print("multiple drops not found")
            
    def verifyDropName(self, dropName, checkingPos):
        #verifyer good enough for now need to add some checking
        left, top, w, h = checkingPos
        text = self.verifyer.getText(left, top, w, h)
        print("Text captured to verify if Drop: %s" % text)
    
        if text == dropName:
            print("SLAYER:VERIFYDROPNAME: Text Verifyed Returning True")
            return True
        else:
            print("SLAYER:VERIFYDROPNAME: Text Not Verifyed Returning False")
            return False
        
    def inArea(self,boundingTile, maxRange):

        if self.verifyer.verifyInArea(self.api,boundingTile=boundingTile,MaxRange=maxRange):
            return True
        else:
            return False
        
     
class ChickenSlayer(Slayer):
    #makesure feathers are highlighted purple on runelite
    #makesure chickens are fully highlighted on runelite
    #make sure opponent info is on (HP)
    from universalMethods import Uni
    drop0name = "Feather"
    drop0Img = 'img/featherText.png'
    textVerificationPos = (41, 32, 58, 17)
    chickenBoundingTile = (3177, 3296)
    boundingRange = 11

    drop0Check = (49,38,53,12)
    left, top, w, h = drop0Check

    feathersInInventory = None
    featherRuneLiteID = 314
    feathersPickedUp = 0
    feathersInventoryLocation = None
    uni = Uni()

    def __init__(self):
        self.monsterName = "Chicken"
        self.chickenOrchestrator()


    def chickenOrchestrator(self):

        while True:
            
            while self.inArea():
                #while within bounds
                self.runner()
                firstPickupAttempts = random.randint(1,5)
                for _ in range(firstPickupAttempts):
                    if self.pickUpDrop(self.drop0name, self.drop0Img, self.textVerificationPos, self.featherRuneLiteID) == None:
                        #this break is making the droppickup logic only pickup once or no times at all
                        break
                self.slay(self.monsterName, self.MONSTERHIGHLIGHT)
                self.pickUpDrop(self.drop0name, self.drop0Img, self.textVerificationPos, self.featherRuneLiteID,)

            self.uni.returnToBoundingArea(self.api, self.chickenBoundingTile, self.boundingRange)
            

        


        #confirm if in range of homing tile
        #openinventtocheck hmfeathers
        #find feather
        #pick up feathers if in range

