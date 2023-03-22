import tkinter as tk
from Globals import Globals as GL
from LabelStandard import LabelStandard

# loading screen for display during program startup
class LoadingScreen(tk.Tk):

    def __init__(self):
        super().__init__()

        # window dimensions
        self.windowWidth = 300
        self.windowHeight = 200

        # users screen dimensions
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()

        # offset variables used when setting window geometry to make window center
        x = int((self.screenWidth/2) - (self.windowWidth/2))
        y = int((self.screenHeight/2) - (self.windowHeight/2))

        # Sets the window to be windowWidth x windowHeight, opening in screen center
        self.geometry(f"{self.windowWidth}x{self.windowHeight}+{x}+{y}")

        # removes window border
        self.overrideredirect(True)

        # makes window fixed size
        self.resizable(False, False)

        # creates a frame that fills the window and will hold all widget and other gui objects
        loadingFrame = tk.Frame(self, background=GL.backgroundColor)
        loadingFrame.pack(side="top", fill="both", expand=True)
        loadingFrame.grid_rowconfigure(0, weight=1)
        loadingFrame.grid_columnconfigure(0, weight=1)

        # Displays a loading text in center of screen
        loadingText = LabelStandard(loadingFrame, labelText="LOADING...")
        loadingText.config(font=GL.fontLarge)
        loadingText.grid()

        # Checks status of finishedLoading variable, destroys window if true, else trys again 1 second later
        self.after(1000, self.checkProgress)

    # checks finishedLoading variable state, closes window if true, rechecks every 1 second
    def checkProgress(self):
        if GL.finishedLoading:
            self.destroy()
        else:
            self.after(1000, self.checkProgress)