import pyautogui
import pygetwindow
import time

inventory = [0] * 28
mouse = None
inventFull = None


def getGame(gameWindowName:str, bottomX, bottomY):
    #finds game window moves to top left and resize to requested value
    #need to add try except
    game_window = pygetwindow.getWindowsWithTitle(gameWindowName)[0]
    game_window.restore()
    game_window.resizeTo(bottomX,bottomY)
    game_window.moveTo(0,0)
    game_window.activate()

    

def main():

    getGame("Runelite", 900,900)

    originX = 726
    originY = 575
    x = originX
    y = originY
    counter = 0
    inventSlotsNotEmpty = 0

    time.sleep(1)

    
    #don't need an array to count
    for i in range(len(inventory)):

        print("RGB X:", x, "Y:",y,"Color:", pyautogui.pixel(x,y))

        if pyautogui.pixel(x,y) != (62,53,41):
            inventSlotsNotEmpty += 1

        counter += 1
        x += 42

        if counter >= 4:
            #print("INVENTFUNCTIONS:CHECKINVENTORYSLOTFORSPECIFICITEM: counter hit 4, resetting counter, x, and increasing y")
            counter = 0
            #sets y for next row
            y += 36
            #sets x back to first column
            x = originX

    print(inventSlotsNotEmpty)

    

if __name__ == "__main__":
    main()
    