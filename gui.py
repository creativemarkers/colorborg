import time
import threading

from tkinter import *
from tkinter import ttk
from tkinter.ttk import *


class Gui:

    scriptSelected = None
    startTime = None
    elapsedTime = None
    labelTime = None
    labelStatus = None
    botName = None
    root = None
    isRunning = False
    scriptStatus = "Testing"

    def __init__(self):
        self.startTime = time.time()
        self.isRunning = True
        pass

    def getDesiredScript(self, scripts:list = [None,"Fisher", "WoodCutter", "Miner"]):
        def on_option_changed(*args):
            self.scriptSelected = selected_option.get()
            root.quit()
            root.destroy()

        root = Tk()
        root.title("Script Selector")

        root.lift()
        root.attributes("-topmost", True)

        selected_option = StringVar(root)
        selected_option.set(scripts[0])

        frm = ttk.Frame(root,padding=15)
        frm.grid()

        ttk.Label(frm, text="Choose a Script").grid(column=0,row=0)

        option_menu = ttk.OptionMenu(frm, selected_option, *scripts)
        option_menu.grid(column=0, row=1)
        option_menu.config(width=15)

        selected_option.trace_add("write", on_option_changed)

        root.mainloop()
    """
    def displayBotInfo(self,botName:str):

        def updateStatus():
            self.labelStatus.config(text=f"Status: {self.scriptStatus}")

        def updateTime():

            self.elapsedTime = round(time.time() - self.startTime)
            formattedTime = self.formatTime()  
            self.labelTime.config(text=f"Running for: {formattedTime}")
            updateStatus()
            self.root.after(1000, updateTime)

        def onClosing():
            
            self.isRunning = False
            self.root.destroy()

        def onPlayClick():
            print("Play Pressed")
        def onPauseClick():
            print("Button was clicked!")
        def onStopClick():
            print("Stop was clicked")

        self.root = Tk()
        self.root.title(botName)

        self.root.geometry("+890+10")
        self.labelTime = ttk.Label(self.root,text="Running for: ")
        self.labelTime.pack()
        self.labelStatus = ttk.Label(self.root, text="Status:")
        self.labelStatus.pack()
        updateTime()
        self.root.protocol("WM_DELETE_WINDOW", onClosing)

    def formatTime(self, seconds = None):

        if seconds == None:
            seconds = self.elapsedTime

        seconds = int(seconds)

        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        formattedTime = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        return formattedTime
    """
if __name__ == "__main__":

    g = Gui()
    g.displayBotInfo("test")
    g.root.mainloop()



