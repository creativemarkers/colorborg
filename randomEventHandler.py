import logging
from mouseFunctions import Mouse
from time import sleep
from utils.fernsUtils import recursiveTruncateRandGauss
from verification import getText, verifyText
from pyautogui import ImageNotFoundException
logger = logging.getLogger(__name__)

NPC_HIGHLIGHTCOLOR = (0,255,255)
RANDOM_EVENT_NPCNAMES = [
    "Bee Keeper", "Capt' Arnav", "Niles", "Miles", "Giles", 
    "Count Check", "Sergeant Damient", "Drunken dwarf", 
    "Evil Bob", "Servant", "Postie Pete", "Molly", "Freaky Forester", 
    "Genie", "Leo", "Dr Jekyll", "Prince", "Princess", "Mysterious Old Man", 
    "Flippa", "Tilt", "Quiz Master", "Rick Turpentine", "Sandwich Lady", 
    "Strange Plant", "Dunce", "Mr. Mordaut"
]

class RandomEventHandler():

    def __init__(self, mouse:Mouse):
        self.mouse = mouse


    def findDismiss(self):
        dismissImgPath = "img/randomEventDismiss.png"
        try:
            x,y = self.mouse.findImageSimple(dismissImgPath)
            return x,y
        except ImageNotFoundException:
            return 0,0


    def dismissRandomEvent(self,x,y):
        """
        rightclick
        find "dismiss"
        click dismiss
        """
        self.mouse.mouseClick(x,y,but="right")
        x,y = self.findDismiss()

        if x == 0 and y == 0:
            logger.info("dismiss not found, someone elses randomevent, returning to normal function")
        else:
            self.mouse.moveMouseToArea(x,y,areaVariance=5,bezier=True)
            sleep(round(recursiveTruncateRandGauss(0.6,0.05,0.7,0.5),4))
            self.mouse.mouseClick(x,y)
            logger.info("dismissed random event")

    def verifyRandomEventNPC(self):
        """
        check against the list of all the random event names, if it's one of them return true
        """
        hoverTextRegion = (8,31,200,20)
        l,t,w,h = hoverTextRegion

        potentialNPCname = getText(l,t,w,h)

        for name in RANDOM_EVENT_NPCNAMES:
            if verifyText(potentialNPCname, name):
                return True
        return False

    def findRandomEventNPC(self):
        try:
            x,y = self.mouse.findColorsIteratively(NPC_HIGHLIGHTCOLOR)
            return x,y
        except TypeError:
            logger.debug("Random Event NPC not found")
            return 0,0
        
    def checkWhenLastChecked(self):
        pass

    def randomEventHandler(self):
        """
        randomEvents happen about once an hour
        check if within 15mins of last check
        check for pixels matching
        if not continue
        decide if we should act afk or not

        need to enable "remove others menu option" from random event plugin
        """
        
        """
        maybe better to only check in an area around me like lets say 2 loops in the find image iteratively
        """

        """
        if last check was not mine
        don't check again for 2 mins, if mine does show up, it will look lik
        if the random event was mine don't check for another 8 mins
        """


        x,y = self.findRandomEventNPC()
        print(x,y)
        if x > 1 or y > 1:
            x,y=self.mouse.moveMouseToArea(x,y,areaVariance=5,bezier=True)
            sleep(round(recursiveTruncateRandGauss(0.6,0.05,0.7,0.5),4))
            if self.verifyRandomEventNPC():
                self.dismissRandomEvent(x,y)
                return True
        else:
            print("random event not found")
            return False

def main():
    sleep(2)
    m =  Mouse()
    reh = RandomEventHandler(m)
    while True:
        reh.randomEventHandler()
        sleep(0.6)
    pass

if __name__ == "__main__":
    main()