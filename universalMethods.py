import random
import time
import pyautogui
from mouseFunctions import Mouse
from verification import Verifyer
from pyautogui import ImageNotFoundException
from inventFunctions import Inventory
from runeliteAPI import RuneLiteApi

class Uni:
    mouse = Mouse()
    ver = Verifyer()
    inv = Inventory()

    def __init__(self):
        pass

    def returnToBoundingArea(self, api, boundingTile, maxRange):
        boundingMarkerColor = (255,115,0)
        region = (0,0,688,726)
        while self.ver.verifyInArea(api,boundingTile=boundingTile, MaxRange=maxRange) == False:
            try:
                mP = self.mouse.findColorsRandomly(boundingMarkerColor, region)
                y,x = mP[0]
                rDur = random.uniform(0.55, 0.87)
                x,y = self.mouse.moveMouseToArea(self, x, y, duration=rDur, areaVariance=8)
                time.sleep(random.uniform(0.1,0.15))
                self.mouse.mouseClick(x,y)
            except IndexError:
                pass
        pass

    def checkBanking(self)->bool:
        #returns bool for to check if banking
        return pyautogui.pixelMatchesColor(550,707,(38,250,43))

    def findBanker(self,bankerColor:tuple,region:tuple)->int:
        #assumes Banker's in camera
        matchingPixels = self.mouse.findColorsRandomly(bankerColor,region)
        y, x = matchingPixels[0] 
        return x, y
    
    def verifyBankBooth(self, verificationString):
        testString = self.ver.getText(0,0,243,53)
        print(testString)
        if self.ver.verifyText(testString, verificationString):
            return True
        else:
            return False

    def clickOnBankBooth(self, bankerColor):
    #function that handles banking at a bank booth
        print("UNIVERSALMETHODS:CLICKONBANKERBOOTH: Attempting to click on bank booth...")
        verificationText = "Bank Bank Booth"
        while not self.checkBanking():
            attempts = 0
            maxAttempts = 4
            while attempts <= maxAttempts:
                if attempts == 4:
                    self.mouse.rotateCameraInRandomDirection("upleft", weightAmount=10)
                try:

                    x, y= self.findBanker(bankerColor,(0,0,527,727))
                    attempts = 5 
                except ImageNotFoundException:
                    attempts += 1
                except IndexError:
                    attempts += 1

                randDur = random.uniform(0.4,0.7)
                x, y = self.mouse.moveMouseToArea(x,y,duration=randDur,areaVariance=5)
                if self.verifyBankBooth(verificationText):
                    self.mouse.mouseClick(x,y)
                    attempts = 5
                    time.sleep(random.randint(5,8))
                elif attempts >= 3:
                    self.mouse.rotateCameraInRandomDirection("down", weightAmount=5)
                    attempts += 1
                else:
                    attempts +=1

    def bankItems(self, itemsBanking, api):
        print("UNIVERSALMETHODS:BANKITEMS: attempting to bank items...")
        itemPos = []
        for itemID in itemsBanking:
            itemPos.append(api.findItemInventory(itemID))
        for item in itemPos:
            self.inv.bankItem(item)
            time.sleep(random.uniform(0.2,0.4))
        
    def verifyBanked(self,itemsBanking,api):
        print("UNIVERSALMETHODS:verifyBanked: attempting to verify items banked")
        items = []
        print(items)
        for itemID in itemsBanking:
            result = api.findItemInventory(itemID)
            if result != None:
                items.append(result)

        if len(items) <= 0:
            return True
        else:
            return False
    
    def closeBank(self):
        self.mouse.moveMouseToArea(567,50,random.uniform(0.3,0.7), areaVariance=8,click=True)
        
    def boothBanker(self, bankerColor:tuple, itemsToBank:list, api:object):
        #handles banking assumes near bank, takes a list of itemIDs,
        #and the api object
        banked = False
        while not banked:
            self.clickOnBankBooth(bankerColor)
            time.sleep(5)
            self.bankItems(itemsToBank,api)
            
            if self.verifyBanked(itemsToBank, api):
                print("Setting banked = true")
                banked = True
                #could also have an option to 
                #click on map back to what ever location
                self.closeBank()

    def clickOnCompass(self):
        self.mouse.moveMouseToArea(732,52,random.uniform(0.4,0.7),areaVariance=12,click=True)

    def directionDecider(self, currPos, desiredPos):

        currentX,currentY = currPos
        desX, desY = desiredPos
        dirDisX = desX - currentX
        dirDisY = desY - currentY
        distX = abs(desX - currentX)
        distY = abs(desY - currentY)

        if dirDisX >= 0:
            xStrDir = "east"
        else:
            xStrDir = "west"

        if dirDisY >= 0:
            yStrDir = "north"
        else:
            yStrDir = "south"

        totalDistance = distX+distY
        diffBetweenXY = abs(distX-distY)
        reqForHalf = totalDistance//2
        print(distX)
        print(distY)


        print(totalDistance)
        print(diffBetweenXY)
        # if distY >= distX:
        #     if dirDisY >= 0:
        #         return "north"
        #     else:
        #         return "south"
        # else:
        #     if dirDisX >= 0:
        #         return "east"
        #     else:
        #         return "west"

    def getCameraFacingDirection(self, currentYaw):
        #yaw ranges
        directions = {
            "northWest" : (128,383),
            "west" :(384,639),
            "southWest" : (640, 895),
            "south" : (896, 1151),
            "southEast" :(1152,1407),
            "east" : (1408,1663),
            "northEast" : (1664,1919)
        }
        for dir, (start,end) in directions.items():
            if start <= currentYaw <= end:
                return dir
        return "north"
    
    def clickAreaDecider(self,desDir,currentFace):

        dirDict = {
            "north"     :0,
            "northWest" :1,
            "west"      :2,
            "southWest" :3,
            "south"     :4,
            "southEast" :5,
            "east"      :6,
            "northEast" :7
        }
        
        compassArray = ["north","northWest","west","southWest","south","southEast","east","northEast"]
        compassDirectionIndex = dirDict[desDir] - dirDict[currentFace]
        
        if compassDirectionIndex <= -1:
            compassDirectionIndex += 8

        print(compassDirectionIndex)
        print("clicking on map area:",compassArray[compassDirectionIndex])
        dirMapCords = {
            "north"     :(810,54),
            "northWest" :(766,71),
            "west"      :(748,114),
            "southWest" :(769,157),
            "south"     :(810,176),
            "southEast" :(848,155),
            "east"      :(871,114),
            "northEast" :(852,71)
        }

        return dirMapCords[compassArray[compassDirectionIndex]]
    
    def moving(self,api):
        status = api.getMovementStatus()

    def coordinateWalker(self,desCoords:tuple,range:int=10):

        api = RuneLiteApi()
        #if within a certain range click on ground
        while not self.ver.verifyInArea(api,desCoords,range):
            #might update the two functions below to only one function to minimize api calls
            curPos = api.getCurrentWorldPosition()
            # print(curPos)
            curYaw = api.getCameraYaw()
            #suggested dir, suggested Yaw
            sDir = self.directionDecider(curPos, desCoords)
            print("should walk in this direction:", sDir)
            curFacing = self.getCameraFacingDirection(curYaw)
            print("currently facing", curFacing)
            x,y = self.clickAreaDecider(sDir,curFacing)
            x,y = self.mouse.moveMouseToArea(x,y,duration=(random.uniform(0.4,0.7)),areaVariance=14)
            time.sleep(random.uniform(0.1,0.2))
            self.mouse.mouseClick(x,y)
            time.sleep(random.randint(5,8))


if __name__ == "__main__":
    c = Uni()
    # print(c.getCameraFacingDirection(383))

    # print(c.clickAreaDecider("south","west"))
    # print(c.clickAreaDecider("northEast","north"))
    # print(c.clickAreaDecider("northEast","east"))
    # print(c.clickAreaDecider("east","northEast"))
    # print(c.clickAreaDecider("north","west"))

    # c.coordinateWalker((3200,3495),5)
            
    c.directionDecider((3109,3433),(3093,3442))
    c.directionDecider((3093,3442),(3109,3433))