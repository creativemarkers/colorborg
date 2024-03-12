import pyautogui
import time
import random

class Camera:

    possibleDirections = ['left','right','up','down']

    def __init__(self):
        pass

    def turnCamera(self, desiredDuration, desiredDirection:str = None):
        
        if desiredDirection != None:
            desiredDirection = random.choice(self.possibleDirections)

        c = random.uniform(0.1,0.3)
        time.sleep(c)
