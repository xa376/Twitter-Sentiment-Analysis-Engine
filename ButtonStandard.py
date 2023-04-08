import tkinter as tk
from Globals import Globals as GL

# default button styling for this program
class ButtonStandard(tk.Button):

    def __init__(self, parent):
        tk.Button.__init__(self, parent)

        self.bind("<Enter>", self.buttonHighlight)
        self.bind("<Leave>", self.buttonRemoveHighlight)
        self.config(font=GL.fontGeneral, background=GL.backgroundColor, foreground=GL.foregroundColor, 
                     activebackground=GL.activeBackgroundColor, activeforeground=GL.activeForegroundColor, 
                      relief=GL.buttonBorder)

    # highlights button when hovered over
    def buttonHighlight(self, event):
        event.widget["background"] = GL.activeBackgroundColor

    # removes highlight from button
    def buttonRemoveHighlight(self, event):
        event.widget["background"] = GL.backgroundColor