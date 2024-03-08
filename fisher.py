from gui import Gui
from inventFunctions import Inventory


class Fisher:

    gui = Gui()
    invent = Inventory()
    selectedSubScript = None
    

    FISHTYPE = [None,"shrimp","lobster","swordfish"]

    def __init__(self):

        self.main()


    def main(self):
        #gui for selection
        self.gui.getDesiredScript(self.FISHTYPE)
        self.selectedSubScript = self.gui.scriptSelected
        print("in fisher main")
        shrimper = ShrimpFisher()
        
        # self.shrimp()
        
        #if statesments to determine which fishing spot is correct

        #select what to fish
        
        #check if invent is full, if full bank, if not go fish
        #fill inventory wish 

    # def shrimp(self):
    #     #load info gui
    #     #log in check
    #     #check if logged in, if not log in or quit run

    #     self.invent.isInventFull(730,567,(178,152,139),27)

    #     #loop runs until invent full
    #     while not self.invent.inventFull:
    #         self.fish()
    #         self.invent.isInventFull(730,567,(178,152,139),27)
    
    def fish(self,type:str):
        pass
        # move mouse()
        # verifyText #will prob make this in another file
        # clickonspot
        # waitTill not fishing
        # back to function that called to verify invent status


    def findFishingSpot():
        #finds fishing spots and verifies it
        pass


class ShrimpFisher(Fisher):

    imglocation = None
    inventoryCheckX = 730
    inventoryCheckY = 567
    colorToCheck = (178,152,139)
    slotsToFill = 27

    def __init__(self):
        self.shrimp()

    def shrimp(self):
        #load info gui
        #log in check
        #check if logged in, if not log in or quit run

        self.invent.isInventFull(730,567,(178,152,139),27)

        #loop runs until invent full
        while not self.invent.inventFull:
            self.fish()
            self.invent.isInventFull(730,567,(178,152,139),27)

    


    
   

    

if __name__ == "__main__":

    main()