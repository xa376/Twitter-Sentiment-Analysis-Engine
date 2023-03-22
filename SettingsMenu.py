import tkinter as tk
from tkinter import ttk
from Globals import Globals as GL
from LabelStandard import LabelStandard

# the programs settings menu
class SettingsMenu(tk.Frame):

    def __init__(self, parent, gui):
        tk.Frame.__init__(self, parent)

        # configures frames grid structure for object positioning
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # settings title label
        self.title = LabelStandard(self, labelText="Settings")
        self.title.grid(row=0, column=0, columnspan=2, sticky="n")

        # max search results option label
        self.resultsLabel = LabelStandard(self, labelText="Max Search Results")
        self.resultsLabel.grid(row=1, column=0, sticky="n", pady=50)

        # all the possible search result options
        resultsValues = [10, 20, 50, 100]

        # initializes an options menu for the max results to show in a search
        self.defaultResults = tk.StringVar(self, value=int(GL.maxResults))
        self.resultsOptions = ttk.OptionMenu(self, self.defaultResults, self.defaultResults.get(), 
                                              *resultsValues, command=self.changeResults)
        self.resultsOptions.grid(row=1, column=0, sticky="n", pady=80)

        # incognito option label
        self.incognitoLabel = LabelStandard(self, labelText="Incognito Mode")
        self.incognitoLabel.grid(row=1, column=1, sticky="n", pady=50)

        # all the possible incognito mode options
        incognitoValues = ["Off", "On"]

        # initializes an options menu for whether or not to save future search history
        self.defaultIncognito = tk.StringVar(self, value="On" if GL.incognitoMode else "Off")
        self.incognitoOptions = ttk.OptionMenu(self, self.defaultIncognito, self.defaultIncognito.get(), 
                                                *incognitoValues, command=self.changeIncognito)
        self.incognitoOptions.grid(row=1, column=1, sticky="n", pady=80)
    
    # toggles incognito mode on/off
    def changeIncognito(self, event):
        GL.incognitoMode = not GL.incognitoMode

    # changes max search results to users selection
    def changeResults(self, event):
        GL.maxResults = int(event)