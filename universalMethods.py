import random
import time
import pyautogui
from mouseFunctions import Mouse
from verification import Verifyer
from pyautogui import ImageNotFoundException


class Uni:
    mouse = Mouse()
    ver = Verifyer()

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

    def bankBoother(self, bankerColor):
        #function that handles banking at a bank booth
        verificationText = "Bank Bank Booth"
        while not self.banking():
            try:
                self.findBanker(bankerColor)
            except ImageNotFoundException:
                pass

    def banking(self)->bool:
        #returns bool for to check if banking
        return pyautogui.pixelMatchesColor(550,707,(38,250,43))


    def findBanker(self,bankerColor:tuple)->int:
        #assumes Banker's in camera
        matchingPixels = self.mouse.findColorsRandomly(bankerColor)
        y, x = matchingPixels[0]
        return y,x
    
    def verifyBanker():
        pass

    def bankItems():
        pass