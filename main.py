
import subprocess
import logging
import sys
from pyautogui import FailSafeException
from gui import Gui
from basicfunctions import Window
from fisher import Fisher
from slayer import Slayer

#initializes gui and game objects to get info for what scripts to run
gui = Gui()
game = Window()

#sets up logging file
logging.basicConfig(filename='errors.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



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

        #calls gui obj to get input for what scripts to run
        # gui.getDesiredScript()

        # #calls script getter
        # scriptGetter(gui.scriptSelected)

        # fisher = Fisher()
        """
        code below disabled for testing
        """

        slayer = Slayer()
        

    #end script gracefully since we have two threads now
    except FailSafeException:
        print("PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED.")
        sys.exit()




#creates appropriate object for the request script    
def scriptGetter(scriptName:str):
    # try:
    #     # ft = ".py"
    #     # fileName = scriptName.lower() + ft
    #     # subprocess.run(["python", fileName])
    #     subprocess.run("fisher.py")
    #     logging.debug("Subprocess output:")
    #     logging.debug(result.stdout)
    #     logging.error("Subprocess error:")
    #     logging.error(result.stderr)
    # except Exception as e:
    #     logging.exception("An unexpected error occurred:")

    fisher = Fisher()

if __name__ == "__main__":
    main()