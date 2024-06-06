import pyautogui
import random
import logging
import keyboard
from time import sleep
from mouseFunctions import Mouse
from runeliteAPI import RuneLiteApi
# from mouseFunctions import moveMouse , findImageSimple
from utils.fernsUtils import recursiveTruncateRandGauss

pyautogui.MINIMUM_DURATION = 0.05

logger = logging.getLogger(__name__)

class Inventory:

    inventory = [0] * 28
    inventEmptyColors = [(62,53,41) for _ in range(28)]
    mouse = None
    inventFull = None

    def __init__(self):
        self.mouse = Mouse()
        self.api = RuneLiteApi()

    def isInventOpen(self):
        result = pyautogui.pixelMatchesColor(765, 825, (113,38,29))
        logger.debug(f"ISINVENTOPEN: checking if invent is open: {result}")
        return result

    def openInvent(self): 
        # move mouse and click on inventory icon or hit escape weight the escape key more
        sleeper = random.uniform(0.3,0.7)
        self.mouse.moveMouseToArea(778, 838, 0.5, 15)
        sleep(sleeper)
        pyautogui.click()
        logger.info("OPENINVENT: clicked on invent")
        sleep(recursiveTruncateRandGauss(0.6,0.1,0.8,0.4))

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
                #print(":CHECKINVENTORYSLOTFORSPECIFICITEM: pixel color matched, setting invent slot to 1")
                self.inventory[i] = 1
            else:
                #print(":CHECKINVENTORYSLOTFORSPECIFICITEM: pixel color did not match, setting invent slot to 0")
                self.inventory[i] = 0

            counter += 1
            x += 42

            if counter >= 4:
                #print(":CHECKINVENTORYSLOTFORSPECIFICITEM: counter hit 4, resetting counter, x, and increasing y")
                counter = 0
                #sets y for next row
                y += 36
                #sets x back to first column
                x = originX

        #print(sum(self.inventory))

    def isInventFull(self, slotsToFull:int):

        while self.isInventOpen() == False:
            logger.info("INVENTFULLSTATUS: opening invent")
            self.openInvent()

        self.checkIfInventSlotsEmpty()

        if sum(self.inventory) >= slotsToFull:
            self.inventFull = True
            return True
        else:
            self.inventFull = False
            return False

    def powerDropInventory(self, doNotDrop:int=0, amountToDrop = 28):
        #doNotDrop is the number of slots to not drop starting from the first slot
        while self.isInventOpen() == False:
            logger.info("INVENTFULLSTATUS: opening invent")
            self.openInvent()

        originX = 726
        x = 726
        y = 575
        shiftPressed = False
        counter = 0
        for i in range(amountToDrop):
            logger.info(f"powering dropping:{amountToDrop}")

            if i >= doNotDrop:
                if shiftPressed == False:
                    pyautogui.keyDown('shift')
                    sleep(random.uniform(0.1,0.2))
                    shiftPressed = True
                dur = round(random.uniform(0.03, 0.075),4)
                self.mouse.moveMouseToArea(x,y,duration=dur,areaVariance=10,click=True)

            counter += 1
            x += 42
            if counter >= 4:
                
                counter = 0
             
                y += 36
                x = originX

        logger.info("finished powerdropping")
        pyautogui.keyUp('shift')

    def dropInventSlot(self,x,y):
        #assumes shift is held
        rDur = round(recursiveTruncateRandGauss(0.04,0.01,0.6,0.025),5)
        rAV = round(recursiveTruncateRandGauss(5,1,10,0))
        # print(f"rDur: {rDur}, rAV: {rAV}")
        x,y = self.mouse.moveMouseToArea(x,y,bezier=True)
        self.mouse.mouseClick(x,y)
        """
        could add a 1%-0.5% chance to double click
        """

    def betterPowerDropper(self, doNotDrop:int=0, amountToDrop=28):
        """
        generate the random pattern (maybe could make multiple patterns)
        apply the pattern in a for loop

        misses are usually because you go to fast,lag
        or miss the target completely
        or failed a click
        the speed needs to be faster
        """

        if amountToDrop == 28:
            amountToDrop = 32
            
        inventSlotCords={
            0: (728, 576), 1: (770, 576), 2: (812, 576), 3: (854, 576), 
            4: (728, 612), 5: (770, 612), 6: (812, 612), 7: (854, 612), 
            8: (728, 648), 9: (770, 648), 10: (812, 648), 11: (854, 648), 
            12: (728, 684), 13: (770, 684), 14: (812, 684), 15: (854, 684), 
            16: (728, 720), 17: (770, 720), 18: (812, 720), 19: (854, 720), 
            20: (728, 756), 21: (770, 756), 22: (812, 756), 23: (854, 756), 
            24: (728, 792), 25: (770, 792), 26: (812, 792), 27: (854, 792)
        }

        generateMisses = round(recursiveTruncateRandGauss(0,0.5,3,0))
        print("BETTERPOWERDROPPER:Misses generated:",generateMisses)
        slotsToMiss = set()
        for i in range(generateMisses):
            slotsToMiss.add(random.randint(doNotDrop,27))
        
        #print("slots missed on purpose", slotsToMiss)

        def doubleRowPattern(doNotDrop:int=0,amountToDrop=32):
            row1 = 0
            row2 = 4

            invArray = self.getFullSlots()
            # print("BETTERPOWERDROPPER:invArray:", invArray)

            for i in range(amountToDrop):
                # print(f"BETTERPOWERDROPPER:i:{i}")
                if i != 0 and i % 8 == 0:
                    row1 = i
                    row2 = i + 4

                if i % 2 == 0:
                    # dropSlot(inventSlotCords[row1])
                    if row1 not in slotsToMiss and row1 >= doNotDrop and row1 in invArray:
                        x,y = inventSlotCords[row1]
                        self.dropInventSlot(x,y)
                        # print("BETTERPOWERDROPPER:dropping slot:", row1)
                    row1 += 1
                else:
                    #redundant arg with row2 inventslotCords
                    # if row2 in inventSlotCords and row2 not in slotsToMiss and row2 >= doNotDrop and row2 in invArray:
                    if row2 not in slotsToMiss and row2 >= doNotDrop and row2 in invArray:
                        x,y = inventSlotCords[row2]
                        self.dropInventSlot(x,y)
                        # print("BETTERPOWERDROPPER:dropping slot:", row2)
                    row2 += 1

        pyautogui.keyDown('shift')
        doubleRowPattern(doNotDrop,amountToDrop)
        sleep(round(recursiveTruncateRandGauss(0.4,0.1,0.8,0.3),4))
        while len(self.getFullSlots()) > doNotDrop:
            print("dropping leftovers")
            invArray = self.getFullSlots()
            for i in range(len(invArray)):
                if invArray[i] >= doNotDrop:
                    x,y = inventSlotCords[invArray[i]]
                    self.dropInventSlot(x,y)
            sleep(0.8)
        pyautogui.keyUp('shift')

    def getFullSlots(self):
        #returns a list of slots that are not empty
        self.api.getInventoryData()
        fullSlots = []
        for i, slot in enumerate(self.api.inventArray):
            if slot['id'] != -1:
                fullSlots.append(i)
        return fullSlots

    def traverseThroughInventory(self, inventSlot:int):

        while self.isInventOpen() == False:
            logger.info("INVENTFULLSTATUS: opening invent")
            self.openInvent()

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
                logger.info("bankItem")
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
        logger.debug(f"items in invent: {sum(self.inventory)}")

    def popDict(self):

        originX = 728
        originY = 576
        x = originX
        y = originY
        counter = 0
        dictI = {}

        for i in range(28):
            dictI[i] = (x,y)

            counter += 1
            x += 42

            if counter >= 4:
                #print("INVENTFUNCTION:CHECKIFINVENTSLOTSEMPTY: counter hit 4, resetting counter, x, and increasing y")
                counter = 0
                #sets y for next row
                y += 36
                #sets x back to first column
                x = originX

        return dictI
    
    def getAmountOfItemsInInvent(self, api:object) -> int:
        api.getInventoryData()
        itemCount = 0
        for item in api.inventArray:
            if item['id'] != -1:
                itemCount += 1
        return itemCount
        
def main():
    import time

    # time.sleep(1)
    i = Inventory()
    # # i.powerDropInventory(1,25)
    # i.powerDropInventory(2,28)

    # result = i.popDict()
    # print(result)

    # print(round(recursiveTruncateRandGauss(0,0.5,3,0))
    time.sleep(1)
    i.betterPowerDropper(2,28)
    # result=i.getFullSlots()
    # print(result)

    # while len(i.getFullSlots()) > 2:
    #     time.sleep(0.6)
    #     print("too much in invent")


if __name__ == "__main__":
    main()


        

            

                








        

        

        
   
        