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

    def slayerOrchestrator(self):
        #move camera fairly often
        pass


    def slay(self, monsterName, monsterHp, monsterHighlightColor):
        pass

        #make sure your monster is highlighted
        #will check runelight plugin hp bar to make sure monster is dead
    
    def checkIfDropsNearby(self, dropColor):
        #bases if nearby based on position of player
        pass

    def pickUpDrops(self):
        #see mouseFunctions.py
        pass
    def verifyDrop(self):
        #see mouseFunctions.py
        pass
        

class chickenSlayer(Slayer):
    #makesure feathers are highlighted purple on runelite
    #makesure chickens are fully highlighted on runelite
    #make sure opponent info is on (HP)
    drop0 = "Feather"
    drop2 = "Bones"
    highlightedDropColor = (170,0,255)
    monsterName = "Chicken"

    def __init__(self):
        self.chickenOrchestrator()

    def chickenOrchestrator(self):
        pass

        self.mouse.findColors(self.highlightedDropColor, 892,727)
        #verify feather
        self.checkIfDropsNearby()
        while self.nothingNearToPickup == True:





        #confirm if in range of homing tile
        #openinventtocheck hmfeathers
        #find feather
        #pick up feathers if in range

