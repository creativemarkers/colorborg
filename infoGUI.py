import time
import logging
import random
from tkinter import *

logger = logging.getLogger(__name__)
class InfoGUI():

    def __init__(self):
        self.scriptStatus = "Waiting for script"
        self.isRunning = True
        self.startTime = time.time()
        self.lastBreak = time.time()
        self.breaks = False

    def main(self, scriptName):
        self.root = Tk()
        self.root.title(scriptName)
        self.root.geometry("+890+10")
        self.timeLabelText = StringVar(self.root)
        self.timeLabelText.set("Running for:")
        self.statusLabelText = StringVar(self.root)
        self.statusLabelText.set(f"Status: {self.scriptStatus}")

        self.timeLabel = Label(self.root, textvariable=self.timeLabelText)
        self.statusLabel = Label(self.root, textvariable=self.statusLabelText)

        #self.button = Button(self.root, text="Click to change the Text", command=self.changeText

        playIconImage = PhotoImage(file="icons/playIcon.png")
        self.playButton = Button(self.root,text="test",image=playIconImage, command=self.onPlayClick)
        pauseIconImage = PhotoImage(file="icons/pauseIcon.png")
        self.pauseButton = Button(self.root,text="test",image=pauseIconImage, command=self.onPauseClick)
        stopIconImage = PhotoImage(file="icons/stopIcon.png")
        self.stopButton = Button(self.root,text="test",image=stopIconImage,command=self.onStopClick)


        self.timeLabel.pack()
        self.statusLabel.pack()
        self.playButton.pack(side=LEFT,ipadx=5,ipady=5,padx=10,pady=5)
        self.pauseButton.pack(side=LEFT,ipadx=5,ipady=5,padx=10,pady=5)
        self.stopButton.pack(side=LEFT,ipadx=5,ipady=5,padx=10,pady=5)

        if self.breaks == True:
            self.takeBreak = False
            self.calculateTimes()
            self.updateTimeWithBreaks()
        else:
            self.updateTime()

        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.root.mainloop()

    def calculateTimes(self,range:tuple = (3,5)):
        l,r = range
        playTimeInHours = random.randint(l,r)
        #print("playTimeInHours:",playTimeInHours)
        playTimeInMinutes = playTimeInHours * 60
        #print("playTimeInMinutes:", playTimeInMinutes)
        randomMinuteOffset = random.choice((-1,1)) * random.randint(1,59)
        # randomMinuteOffset = random.randint(1,30)
        #print("RandomMinuteOffset:",randomMinuteOffset)
        realPlayTime = playTimeInMinutes + randomMinuteOffset
        #print("realPlayTime:",realPlayTime)
        # print(f"hour:{realPlayTime//60}, minutes: {realPlayTime%60}")

        # print(realPlayTime*60)

        # return realPlayTime * 60

        self.suggestedPlayTime = realPlayTime * 60
        #print("suggestedPlayTime:",self.suggestedPlayTime)
        
    def onClosing(self):
        self.isRunning = False
        self.root.destroy()

    def onPlayClick(self):
        print("hi")
    
    def onPauseClick(self):
        print("paused")

    def onStopClick(self):
        logger.critical("STOP BUTTON CLICKED KILLING SCRIPT")
        self.isRunning = False
        self.root.destroy()

    def updateStatus(self):
        self.statusLabelText.set(f"Status: {self.scriptStatus}")

    def updateTime(self):
        self.elapsedTime = round(time.time()-self.startTime)
        formattedTime = self.formatTime()
        self.timeLabelText.set(f"Running for: {formattedTime}")
        self.updateStatus()
        self.root.after(1000,self.updateTime)

    def updateTimeWithBreaks(self):
        self.elapsedTime = round(time.time()-self.startTime)
        formattedTime = self.formatTime()
        self.timeLabelText.set(f"Running for: {formattedTime}")
        
        self.timeSinceLastBreak = round(time.time()-self.lastBreak)
        if self.takeBreak == False and self.timeSinceLastBreak >= self.suggestedPlayTime:
            self.breakTime = round(self.suggestedPlayTime / random.uniform(1.5,2))
            #print("breakTime:",self.breakTime)
            self.takeBreak = True

        self.updateStatus()
        self.root.after(1000,self.updateTimeWithBreaks)

    def formatTime(self, seconds = None):

        if seconds == None:
            seconds = self.elapsedTime

        seconds = int(seconds)

        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        formattedTime = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        return formattedTime

# g = InfoGUI()
# g.calculateTimes((0,0))
# # # g.main("test")
# # # g = GUI()
# # # time.sleep(2)

# # # g.scriptStatus("test")

# # print(round(10860/1.39))

# # print(10860/1.39)