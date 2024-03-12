import time

from tkinter import *
from tkinter import ttk


class Gui:

    scriptSelected = None
    startTime = None
    elapsedTime = None
    labelTime = None
    botName = None
    root = None

    def __init__(self):
        self.startTime = time.time()
        pass

    def getDesiredScript(self, scripts:list = [None,"Fisher", "WoodCutter", "Miner"]):
        def on_option_changed(*args):
            self.scriptSelected = selected_option.get()
            root.quit()

        # options = [None,"Fisher", "WoodCutter", "Miner"]
        root = Tk()
        root.title("Script Selector")

        root.lift()
        root.attributes("-topmost", True)


        selected_option = StringVar(root)
        selected_option.set(scripts[0])


        frm = ttk.Frame(root,padding=15)
        frm.grid()

        ttk.Label(frm, text="Choose a Script").grid(column=0,row=0)
        # ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0,row=1)
        # ttk.OptionMenu(frm, selected_option, *scripts).grid(column=0,row=2)

        option_menu = ttk.OptionMenu(frm, selected_option, *scripts)
        option_menu.grid(column=0, row=1)
        option_menu.config(width=15)

        selected_option.trace_add("write", on_option_changed)

        # print(selected_option.get())

        root.mainloop()

    def displayBotInfo(self,botName:str):

        def updateTime():
            self.elapsedTime = round(time.time() - self.startTime)    
            self.labelTime.config(text=f"Script has been running for: {self.elapsedTime} seconds")
            self.root.after(1000, updateTime)

        self.root = Tk()
        self.root.title(botName)
        #sets the location of the gui
        self.root.geometry("+890+10")
        self.labelTime = ttk.Label(self.root,text="Script has been running for: 0 seconds")
        self.labelTime.pack()
        updateTime()
        #root.mainloop()




