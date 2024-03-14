import pyautogui
import time
import random

class Camera:

    possibleDirections = ['left','right','up','down']
    lastFakeTurnCount = 0

    def __init__(self):
        pass

    def turnCameraWithKeyBoard(self, desiredDuration = 1.0, desiredDirection:str = None):
        
        if desiredDirection == None:
            direction = random.choice(self.possibleDirections)
        else:
            direction = desiredDirection

        if desiredDuration == 1.0:
            duration = random.uniform(.75,1.5)
        else:
            duration = desiredDuration

        c = random.uniform(0.05,0.2)
        time.sleep(c)
        print("CAMERA:TURNCAMERAWITHKEYBOARD: turning camera in",direction,"direction.")
        pyautogui.keyDown(direction)
        time.sleep(duration)
        pyautogui.keyUp(direction)

    def turnCameraWithMouse(self, desiredDuration = 1.0, desiredDirection:str = None):
        pass
        #place holder function for when creating a turning camera for mouse as that seems more realistic 
        
        # if desiredDirection != None:
        #     direction = random.choice(self.possibleDirections)
        # else:
        #     direction = desiredDirection

        # if desiredDuration == 1.0:
        #     duration = random.uniform(.75,1.5)
        # else:
        #     duration = desiredDuration

        # c = random.uniform(0.05,0.2)
        # time.sleep(c)
        
        # pyautogui.keyDown(direction)
        # time.sleep(duration)
        # pyautogui.keyUp(direction)

    def humanCameraBehavior(self, desiredRange):
        #desired range is used to determine the weighting of the chance for the camera to turn for example, 10, will have a 10% chance for camera to turn
        
        print("CAMERA:HUMANCAMERABEHAVIOR:checking if camera should turn")

        if self.lastFakeTurnCount >= desiredRange:
            print("CAMERA:HUMANCAMERABEHAVIOR: counter higher than desired range, camera turning...")
            self.lastFakeTurnCount = 0
            self.turnCameraWithKeyBoard()

        else:
            denominator = 2
            weightIncreaser = self.lastFakeTurnCount // denominator
            moddedRange = desiredRange - weightIncreaser

            trigger = moddedRange//2
            number = random.randint(1,moddedRange)

            if number == trigger:
                print("CAMERA:HUMANCAMERABEHAVIOR: camera turning...")
                self.lastFakeTurnCount = 0
                self.turnCameraWithKeyBoard()

            else:
                self.lastFakeTurnCount += 1