import logging
import sys
from pyautogui import FailSafeException
from gui import Gui
from osFunctions import Window
from fisher import Fisher
from slayer import Slayer
from logOrganizer import LogOrganizer

#initializes gui and game objects to get info for what scripts to run
gui = Gui()
game = Window()

def createBot(scriptName:str):

    bot = globals().get(scriptName)
    return bot()

def main():
    # # pyautogui.FAILSAFE = True
    try:

        game.getGame("Runelite", 900,900)

        '''
        pseudo code starts
        '''
        #checks if logged in
        #attempts to log in if not
        #check if trying to login to members world if not member
        #calls gui to get more info about scripts to run
        '''
        pseudo code ends
        '''

        """
        code below disabled for testing
        """
        #calls gui obj to get input for what scripts to run, going to include if user wants logging, enabled by default
        availableScripts = [None, "Fisher", "Slayer"]
        gui.getDesiredScript(availableScripts)
        lScript = gui.scriptSelected.lower()
        log = LogOrganizer(lScript)
        log.setupDirectory()
        logFileName = lScript + "_log.log"
        #print(logFileName)
        logging.basicConfig(level=logging.DEBUG, filename= logFileName, filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        logging.debug(f"{gui.scriptSelected.upper()} SELECTED")
        createBot(gui.scriptSelected)

        

        #fisher = Fisher()
        #slayer = Slayer()

    #end script gracefully since we have two threads now
    except FailSafeException:
        print("PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED.")
        sys.exit()

if __name__ == "__main__":
    main()