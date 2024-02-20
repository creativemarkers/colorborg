import pyautogui
import time
from basicfunctions import getGame
from mouseFunctions import moveMouse , findImageSimple
#from pyclick import HumanClicker
#from mouseFunctions import move_mouse_with_bezier
#from mouse import move_to_img

def main():
    pyautogui.FAILSAFE = True
    # getGame("Runelite", 900,900)
    # moveMouse(1000, 500, 1)

    findImageSimple('img/test.png', .9)


    # if login == True and atLocation == True:

if __name__ == "__main__":
    main()