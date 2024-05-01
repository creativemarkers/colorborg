import time
import threading

from tkinter import *
# from tkinter import ttk
from tkinter.ttk import *


class Gui:

    startTime = None
    elapsedTime = None
    labelTime = None
    labelStatus = None
    botName = None
    root = None
    isRunning = False
    scriptStatus = "Testing"

    def __init__(self):
        self.scriptSelected = None
        self.startTime = time.time()
        self.isRunning = True
        self.breaks = False
        pass

    def getDesiredScript(self, scripts:list = [None,"Fisher", "WoodCutter", "Miner"]):
        def onSubmitClick():
            if v.get() == "1":
                self.breaks = True

            self.scriptSelected = selected_option.get()
            print(self.scriptSelected)
        

            root.quit()
            root.destroy()
            return self.scriptSelected

        root = Tk()
        root.title("Script Selector")

        root.lift()
        root.attributes("-topmost", True)

        selected_option = StringVar(root)
        selected_option.set(scripts[0])

        frm = Frame(root,padding=10)
        frm.grid()

        scriptLabel = Label(frm, text="Choose a Script").grid(column=0,row=0)

        option_menu = OptionMenu(frm, selected_option, *scripts)
        option_menu.grid(column=0, row=2, pady=(10,0))
        option_menu.config(width=15)

        v = StringVar(root, "1")

        values = {
            "Breaks":"1",
            "No Breaks": "2",
        }

        for (text,value) in values.items():
            Radiobutton(root, text=text, variable=v,
                        value=value).grid(column=0,row=int(value)+2)
            
        submitButton = Button(root,text="Submit",command=onSubmitClick)

        submitButton.grid(column=0, row=5)

        # v.trace_add("write",onButtonChange)

        # selected_option.trace_add("write", on_option_changed)

        root.mainloop()

if __name__ == "__main__":

    g = Gui()
    g.getDesiredScript()


