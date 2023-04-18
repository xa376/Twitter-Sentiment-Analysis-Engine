import tkinter as tk
from tkinter import ttk
from Globals import Globals as GL
from ButtonStandard import ButtonStandard
from LabelStandard import LabelStandard

# the programs history menu
class HistoryMenu(tk.Frame):

    def __init__(self, parent, gui):
        tk.Frame.__init__(self, parent)

        # history title display
        self.title = LabelStandard(self, labelText="History")
        self.title.grid(row=0, column=0)

        # frame that will hold the history display box and its scrollbar
        self.historyBoxFrame = ttk.Frame(self)
        self.historyBoxFrame.grid(row=1, column=0, padx=10)

        # initializes a listbox in the history box frame, this box will display users history
        self.historyBox = tk.Listbox(self.historyBoxFrame, height=17, width=73, font=GL.fontGeneral, 
                                     background=GL.activeBackgroundColor, foreground=GL.foregroundColor,
                                      selectforeground=GL.activeForegroundColor, selectbackground=GL.listSelectedColor)
        self.historyBox.pack(side="left", fill="y")

        # inserts search history into the history box
        for line in GL.searchHistory:
            self.historyBox.insert(tk.END, line)

        # places a scrollbar in the history frame
        scrollBar = tk.Scrollbar(self.historyBoxFrame, orient="vertical")
        scrollBar.config(command=self.historyBox.yview)
        scrollBar.pack(side="right", fill="y")

        # makes the scrollbar work on the history box
        self.historyBox.config(yscrollcommand=scrollBar.set)

        # button that when pressed deletes the selected history from the history box
        self.deleteButton = ButtonStandard(self)
        self.deleteButton.config(text="Delete", command=self.deleteHistory)
        self.deleteButton.grid(row=2, column=0, pady=5)

    # updates historybox with any new history in searchHistory
    # occurs every time frame is opened
    def updateHistory(self, event=None):
        self.historyBox.delete(0, tk.END)
        for line in GL.searchHistory:
            self.historyBox.insert(tk.END, line)
        return

    # deletes the selected history from the history box
    def deleteHistory(self, event=None):

        # leaves if search history is empty or no search history is selected
        if not GL.searchHistory or not self.historyBox.curselection():
            return

        # gets the selected text string
        text = self.historyBox.get(self.historyBox.curselection()[0])

        # removes the selected text from programs search history
        GL.searchHistory.discard(text)

        # removes the selected text from the historyBox
        self.historyBox.delete(self.historyBox.curselection()[0])
        
        return