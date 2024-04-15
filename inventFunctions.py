import pyautogui
import random
from time import sleep
from mouseFunctions import Mouse
# from mouseFunctions import moveMouse , findImageSimple
class Inventory:

    inventory = [0] * 28
    inventEmptyColors = [(62,53,41) for _ in range(28)]
    mouse = None
    inventFull = None

    def __init__(self):
        self.mouse = Mouse()

    def isInventOpen(self):
        print("INVENTFUNCTIONS: ISINVENTOPEN: checking if invent is open:", pyautogui.pixelMatchesColor(765, 825, (113,38,29)))
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

    def checkInventorySlotForSpecificItem(self,originX:int,originY:int,color:tuple,):
        #NOT USED AT THE MOMEMNT

        #need to get coordinates of first items color and pixel
        x = originX
        y = originY
        counter = 0


        #don't need an array to count
        for i in range(len(self.inventory)):

            if self.checkItemInInventSlot(x,y,color) == True:
                #print("INVENTFUNCTIONS:CHECKINVENTORYSLOTFORSPECIFICITEM: pixel color matched, setting invent slot to 1")
                self.inventory[i] = 1
            else:
                #print("INVENTFUNCTIONS:CHECKINVENTORYSLOTFORSPECIFICITEM: pixel color did not match, setting invent slot to 0")
                self.inventory[i] = 0

            counter += 1
            x += 42

            if counter >= 4:
                #print("INVENTFUNCTIONS:CHECKINVENTORYSLOTFORSPECIFICITEM: counter hit 4, resetting counter, x, and increasing y")
                counter = 0
                #sets y for next row
                y += 36
                #sets x back to first column
                x = originX

        print(sum(self.inventory))

    def isInventFull(self, slotsToFull:int):

        while self.isInventOpen() == False:
            print("INVENTFUNCTIONS:INVENTFULLSTATUS: opening invent")
            self.openInvent()

        self.checkIfInventSlotsEmpty()

        if sum(self.inventory) >= slotsToFull:
            self.inventFull = True
            return True
        else:
            self.inventFull = False
            return False

    def powerDropInventory(self, doNotDrop:int=0):
        #doNotDrop is the number of slots to not drop starting from the first
        originX = 726
        x = 726
        y = 575
        shiftPressed = False
        counter = 0

        for i in range(len(self.inventory)):

            if i >= doNotDrop:
                if shiftPressed != True:
                    pyautogui.keyDown('shift')
                    shiftPressed = True
                dur = random.uniform(0.1, 0.2)
                self.mouse.moveMouseToArea(x,y,duration=dur,areaVariance=10,click=True)

            counter += 1
            x += 42

            if counter >= 4:
                #print("INVENTFUNCTIONS:POWERDROPINVENTORY: counter hit 4, resetting counter, x, and increasing y")
                counter = 0
                #sets y for next row
                y += 36
                #sets x back to first column
                x = originX

        pyautogui.keyUp('shift')
        shiftPressed=True

    def traverseThroughInventory(self, inventSlot:int):

        originX = 726
        x = 726
        y = 575
        counter = 0

        for i in range(len(self.inventory)):

            if i == inventSlot:
                dur = random.uniform(0.1, 0.2)
                #self.mouse.moveMouseToArea(x,y,duration=dur,areaVariance=10,click=True)
                self.mouse.moveMouseToArea(x,y,duration=dur,areaVariance=10)

            counter += 1
            x += 42

            if counter >= 4:
                counter = 0
                y += 36
                x = originX

    def bankItem(self, inventSlot:int):

        originX = 726
        x = 726
        y = 575
        counter = 0

        for i in range(len(self.inventory)):

            if i == inventSlot:
                dur = random.uniform(0.2, 0.3)
                #self.mouse.moveMouseToArea(x,y,duration=dur,areaVariance=10,click=True)
                x,y = self.mouse.moveMouseToArea(x,y,duration=dur,areaVariance=10)
                self.mouse.mouseClick(x,y,but='right')
                y += 85
                dur = random.uniform(0.3, 0.45)
                x,y = self.mouse.moveMouseToArea(x,y,dur,areaVariance=2)
                self.mouse.mouseClick(x,y)
                print("INVENTFUNCTIONS:bankItem")
                return None

            counter += 1
            x += 42

            if counter >= 4:
                counter = 0
                y += 36
                x = originX

    def checkIfInventSlotsEmpty(self):

        originX = 726
        originY = 575
        x = originX
        y = originY
        counter = 0

        for i in range(28):
            if pyautogui.pixel(x,y) == (62,53,41):
                #print("Invent slot %s is empty" %i)
                self.inventory[i] = 0
            else:
                #print("Invent slot %s is not empty" %i)
                self.inventory[i] = 1

            counter += 1
            x += 42

            if counter >= 4:
                #print("INVENTFUNCTION:CHECKIFINVENTSLOTSEMPTY: counter hit 4, resetting counter, x, and increasing y")
                counter = 0
                #sets y for next row
                y += 36
                #sets x back to first column
                x = originX
        print(sum(self.inventory))



        

            

                








        

        

        
   
        