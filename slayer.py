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

    MONSTERHIGHLIGHT = (0,255,255)

    def __init__(self):
        self.main()

    def main(self):
        pass
        #startThreads


        #get which attack style to prio?

        # self.botThread = threading.Thread(target = self.createBot, args=("shrimp",))
        # self.botThread.start()
        # #creates display gui, then creates thread and starts it
        # self.infoGUI.displayBotInfo("Shrimp PowerFisher")
        # self.infoGuiThread = threading.Thread(target = self.infoGUI.root.mainloop())
        # self.infoGuiThread.start()
    
        #check if running(in game)

    def slayerOrchestrator(self):
        #move camera fairly often
        pass


    def slay(self, monsterName, monsterHp, monsterHighlightColor):
        pass

        #make sure your monster is highlighted
        #will check runelight plugin hp bar to make sure monster is dead
    
    def runner(self):

        #handles running
        runningColor = (206,168,1)
        x, y = 742, 164

        if pyautogui.pixelMatchesColor(x, y, runningColor) == False:
            print("SLAYER:RUNNER: Not running")
            runningThreshold = random.randint(50, 80)
            currentRunEnergy = int(self.verifyer.getText(702,163, 16, 11))
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

    def pickUpDrops(self):
        pass

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

    def verifyDrop(self, dropName, checkingPos):
        left, top, w, h = checkingPos
        text = self.verifyer.getText(left, top, w, h)
        print("Text captured to verify if Drop: %s" %text)

        if text == dropName:
            return True
        else:
            return False
        

class chickenSlayer(Slayer):
    #makesure feathers are highlighted purple on runelite
    #makesure chickens are fully highlighted on runelite
    #make sure opponent info is on (HP)
    drop0name = "Feather"
    drop0Img = 'img/featherText.png'
    

    drop0Check = (49,38,53,12)
    left, top, w, h = drop0Check

    def __init__(self):
        self.monsterName = "Chicken"
        self.chickenOrchestrator()


    def chickenOrchestrator(self):
        pass

        #verify feather
        
        while True:


            feathersToPickup = random.randint(1,4) + self.monsterSlain
            

            self.runner()
            #choose to only pickup nearby or further drops
            self.pickUpNearbyDrops(self.drop0name, self.drop0Img, feathersToPickup)

            slay between 1-3 chickens

            decide if further feathers should be pickedUp(pretty likely)


    





        #confirm if in range of homing tile
        #openinventtocheck hmfeathers
        #find feather
        #pick up feathers if in range

