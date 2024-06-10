import logging
from mouseFunctions import Mouse
from time import sleep
from utils.fernsUtils import recursiveTruncateRandGauss
from verification import getText, verifyText
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


    def dismissRandomEvent(self,x,y):
        print("it verified")
        pass


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
            print("going in her")
            x,y = self.mouse.findColorsIteratively(NPC_HIGHLIGHTCOLOR)
            print("from find random event npc:",x,y)
            return x,y
        except TypeError:
            logger.debug("Random Event NPC not found")
            return 0,0

    def randomEventHandler(self):
        """
        randomEvents happen about once an hour
        check if within 15mins of last check
        check for pixels matching
        if not continue
        decide if we should act afk or not

        need to enable "remove others menu option" from random event plugin
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
    sleep(1)
    m =  Mouse()
    reh = RandomEventHandler(m)
    x,y = reh.findRandomEventNPC()
    print(x,y)
    reh.randomEventHandler()
    pass

if __name__ == "__main__":
    main()