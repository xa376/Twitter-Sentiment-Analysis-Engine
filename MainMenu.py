import tkinter as tk
from Globals import Globals as GL
from SearchMenu import SearchMenu
import os.path
from ButtonStandard import ButtonStandard
from LabelStandard import LabelStandard

# the programs main menu
class MainMenu(tk.Frame):

    def __init__(self, parent, gui):
        tk.Frame.__init__(self, parent)

        # initializes a class variable of the main menu image if it's found
        if os.path.exists("./image_main.png"):
            self.icon = tk.PhotoImage(file='image_main.png', height=250, width=400)
        else:
            print("Main menu image not found.")
            self.icon = tk.PhotoImage(height=250, width=400)

        # configures frames grid structure for object positioning
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # displays main menu title
        self.title = LabelStandard(self, labelText="Main Menu")
        self.title.config(font=GL.fontLarge)
        self.title.grid(row=0, pady=5)

        # displays the main menu image
        self.canvas = tk.Canvas(self, background=GL.backgroundColor, borderwidth=0, highlightthickness=0)
        self.canvas.create_image(0, 0, anchor="nw", image=self.icon)
        self.canvas.grid(row=1, columnspan=2)
        
        # button that takes user to search menu
        self.searchButton = ButtonStandard(self)
        self.searchButton.config(text="Search", font=GL.fontLarge, command=lambda: gui.showFrame(SearchMenu))
        self.searchButton.grid(row=2, sticky="ns", pady=30)