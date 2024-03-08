import pyautogui
import random
from time import sleep
from mouseFunctions import Mouse
# from mouseFunctions import moveMouse , findImageSimple
class Inventory:

    inventory = [0] * 28
    mouse = None
    inventFull = None

    def __init__(self):
        self.mouse = Mouse()

    def isInventOpen(self):
        print("INVENTFUNCTIONS: ISINVENTOPEN: checking if invent is open")
        return pyautogui.pixelMatchesColor(765, 825, (113,38,29))

    def openInvent(self): 
        # move mouse and click on inventory icon or hit escape weight the escape key more
        sleeper = random.uniform(0.3,0.7)
        self.mouse.moveMouseToArea(778, 838, 0.5, 15)
        sleep(sleeper)
        pyautogui.click()
        print("INVENTFUNCTIONS: OPENINVENT: clicked on invent")

    def checkItemInInventSlot(self, x,y,color:tuple):
        return pyautogui.pixelMatchesColor(x,y,color) 

    def checkInventorySlotForSpecificItem(self,originX:int,originY:int,color:tuple):
        #STILL NEEDS TESTING!!

        #need to get coordinates of first items color and pixel
        x = originX
        y = originY
        counter = 0


        #don't need an array to count
        for i in range(len(self.inventory)):

            if self.checkItemInInventSlot(x,y,color) == True:
                print("INVENTFUNCTIONS:CHECKINVENTORYSLOTFORSPECIFICITEM: pixel color matched, setting invent slot to 1")
                self.inventory[i] = 1
            else:
                print("INVENTFUNCTIONS:CHECKINVENTORYSLOTFORSPECIFICITEM: pixel color did not match, setting invent slot to 0")
                self.inventory[i] = 0

            counter += 1
            x += 42

            if counter >= 4:
                print("INVENTFUNCTIONS:CHECKINVENTORYSLOTFORSPECIFICITEM: counter hit 4, resetting counter, x, and increasing y")
                counter = 0
                #sets y for next row
                y += 36
                #sets x back to first column
                x = originX

        

    def isInventFull(self,x:int,y:int,color:tuple,slotsToFull:int):

        while self.isInventOpen() == False:
            print("INVENTFUNCTIONS:INVENTFULLSTATUS: opening invent")
            self.openInvent()

        self.checkInventorySlotForSpecificItem(x,y,color)

        if sum(self.inventory) >= slotsToFull:
            self.inventFull = True
        else:
            self.inventFull = False

        

        
   
        