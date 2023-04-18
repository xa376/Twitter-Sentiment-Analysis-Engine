import tkinter as tk
from Globals import Globals as GL

# default label styling for this program
class LabelStandard(tk.Label):

    def __init__(self, parent, labelText="None"):
        tk.Label.__init__(self, parent)

        # styles label with the global styles
        self.config(text=labelText, font=GL.fontGeneral, background=GL.backgroundColor, foreground=GL.foregroundColor)