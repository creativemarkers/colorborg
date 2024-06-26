import pygetwindow
import os

class Window:

    def getGame(self, gameWindowName:str, bottomX, bottomY):
        #finds game window moves to top left and resize to requested value
        #need to add try except
        game_window = pygetwindow.getWindowsWithTitle(gameWindowName)[0]
        game_window.restore()
        game_window.resizeTo(bottomX,bottomY)
        game_window.moveTo(0,0)
        game_window.activate()

def countFiles(folderPath:str):

    fileCount = 0
    for _,_, files in os.walk(folderPath):
        fileCount += len(files)
    return fileCount

    

