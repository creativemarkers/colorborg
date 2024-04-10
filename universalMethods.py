import random
import time
import pyautogui
from mouseFunctions import Mouse
from verification import Verifyer
from pyautogui import ImageNotFoundException
from inventFunctions import Inventory

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
            randDur = random.uniform(0.4,0.7)
            x, y = self.mouse.moveMouseToArea(x,y,duration=randDur,areaVariance=5)
            if self.verifyBankBooth(verificationText):
                self.mouse.mouseClick(x,y)

    def bankItems(self, itemsBanking, api):
        itemPos = []
        for itemID in itemsBanking:
            itemPos.append(api.findItemInventory(itemID))
        for item in itemPos:
            self.inv.bankItem(item)
            time.sleep(random.uniform(0.2,0.4))

    def boothBanker(self, bankerColor:tuple, itemsToBank:list, api:object):
        #handles banking assumes near bank, takes a list of itemIDs,
        #and the api object
        banked = False
        while not banked:
            self.clickOnBankBooth(bankerColor)
            time.sleep(5)
            self.bankItems(itemsToBank,api)
            #result = self.validateBanked
            #need to close bank
            #could also have an option to just click on map back to what ever location
    
            banked = True
        
