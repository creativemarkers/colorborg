from tkinter import *
from tkinter import ttk


class Gui:

    scriptSelected = None

    def __init__(self):
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





