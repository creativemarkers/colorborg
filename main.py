import pyautogui
import time
from basicfunctions import getGame
from mouseFunctions import moveMouse
#from pyclick import HumanClicker
#from mouseFunctions import move_mouse_with_bezier
#from mouse import move_to_img

def main():
    pyautogui.FAILSAFE = True
    #getGame("Runelite", 900,900)
    moveMouse(1000, 500, 1)

    # if login == True and atLocation == True:

if __name__ == "__main__":
    main()