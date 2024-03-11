
import subprocess
import logging
from gui import Gui
from basicfunctions import Window
from fisher import Fisher

#initializes gui and game objects to get info for what scripts to run
gui = Gui()
game = Window()

#sets up logging file
logging.basicConfig(filename='errors.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



def main():
    # # pyautogui.FAILSAFE = True
    game.getGame("Runelite", 900,900)

    #calls gui obj to get input for what scripts to run
    # gui.getDesiredScript()

    # #calls script getter
    # scriptGetter(gui.scriptSelected)

    fisher = Fisher()



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