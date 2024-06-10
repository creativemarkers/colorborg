import logging
import sys
from pyautogui import FailSafeException
from gui import Gui
from osFunctions import Window
from fisher import Fisher
from slayer import Slayer
from utils.logOrganizer import LogOrganizer
from datetime import datetime

#initializes gui and game objects to get info for what scripts to run
gui = Gui()
game = Window()

MAX_LOG_AGE = 90
#MAX_LOG_AGE Represents the amount of days logs should be kept

def createBot(scriptName:str):

    bot = globals().get(scriptName)
    return bot()

def main():
    
    try:
        game.getGame("Runelite", 900,900)

        #calls gui obj to get input for what scripts to run, going to include if user wants logging, enabled by default atm
        availableScripts = ["Fisher", "Slayer"]

        gui.getDesiredScript(availableScripts)

        lScript = gui.scriptSelected.lower()

        log = LogOrganizer(lScript)

        log.setupDirectory()

        logNameTrailer = datetime.now().strftime("_log_%H_%M_%S.log")

        logFileName = lScript + logNameTrailer

        todaysLogFilePath = log.getTodaysLogFolderPath()

        logFilePath = todaysLogFilePath + "\\"+ logFileName
        
        log.deleteLogsAfterSetDays(MAX_LOG_AGE)

        logging.basicConfig(level=logging.DEBUG, filename= logFilePath, filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        logging.info(f"{gui.scriptSelected.upper()} SELECTED")

        createBot(gui.scriptSelected)

    #end script gracefully since we have two threads now
    except FailSafeException:
        print("PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED.")
        sys.exit()

if __name__ == "__main__":
    main()