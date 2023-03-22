import tkinter as tk
from tkinter import ttk
from Globals import Globals as GL

# input window that gives predictive text options
class InputWindow(tk.Toplevel):

    def __init__(self, parent, event=None):
        tk.Toplevel.__init__(self, parent)

        # sets parent window
        self.parent = parent

        # sets window styling
        self.config(background=GL.backgroundColor)

        # Makes main window untouchable (user can only interact with this one)
        self.grab_set()

        # makes window not resizable
        self.resizable(False, False)

        # holds the text in the input box, to insert into main windows input box after this window destroyed
        self.searchWindowInputBoxText = tk.StringVar()
        self.searchWindowInputBoxText.set("")

        # initializes the search windows user input box
        self.searchWindowInputBox = ttk.Entry(self, textvariable=self.searchWindowInputBoxText, width=64, font=GL.fontGeneral)
        self.searchWindowInputBox.pack()

        # moves the users focus from the input box to the predictive words box using down arrow
        self.searchWindowInputBox.bind("<Down>", self.moveToListBox)

        # populates the predictive text options every time a user presses a key in the input box
        self.searchWindowInputBoxText.trace('w', self.predict)

        # closes the window when the user presses enter
        self.searchWindowInputBox.bind("<Return>", lambda event=None: self.destroy())

        # text box underneath search window to hold predicted text suggestions
        self.predictedTextBox = tk.Listbox(self, height=10, width=64, font=GL.fontGeneral, 
                                            background=GL.activeBackgroundColor, foreground=GL.foregroundColor, 
                                             selectforeground=GL.activeForegroundColor, selectbackground=GL.listSelectedColor)
        self.predictedTextBox.pack()

        # adds the current selected predictive word to the users input box
        self.predictedTextBox.bind("<Right>", self.addWord)

        # sets the search window input box text to initially be the main windows input box text
        self.searchWindowInputBox.insert(0, parent.searchInputBox.get())

        # sets main windows input box text to this windows text on destroy
        self.searchWindowInputBox.bind("<Destroy>", self.onDestroy)

        # after button press event has finished sets focus to inputbox
        self.after(1, self.searchWindowInputBox.focus)


    # predicts then updates predicted text box with predicted text
    def predict(self, event, b, c):

        # Clears previously predicted text
        self.predictedTextBox.delete(0, tk.END)
        predictedWords = set()

        # gets the current word being typed, then fills the predictedWords set with suggestions from the trie
        GL.allWords.predict(self.getCurrWord(event), predictedWords)

        # displays the predicted words in the predicted text box
        for word in predictedWords:
            self.predictedTextBox.insert(tk.END, word)

        return

    # gets the current word being type from the search windows input box
    def getCurrWord(self, event):

        userInput = self.searchWindowInputBoxText.get()

        # sets starting index to last index of users input
        i = -1
        currWord = ""

        # iterates from the end of the users input, storing each letter in currWord, stopping when
        # a letter or number is no longer found
        while i >= -len(userInput) and str.isalnum(userInput[i]):
            currWord = userInput[i] + currWord
            i-=1

        # returns the last word
        return currWord

    # Adds the selected predicted word to the search input box
    def addWord(self, event=None):

        # gets selected word from predicted text box
        wordToAdd = self.predictedTextBox.get(self.predictedTextBox.curselection()[0])

        # gets users input before selecting a predicted word
        prevWords = self.searchWindowInputBoxText.get()

        # removes the current last word from the users input, the selected word will be placed here
        prevWords = prevWords[:len(prevWords) - len(self.getCurrWord(event))]

        # clears predicted text
        self.predictedTextBox.delete(0, tk.END)

        # sets the search windows input box to the previous words plus the new word
        self.searchWindowInputBox.delete(0, tk.END)
        self.searchWindowInputBox.insert(0, prevWords + wordToAdd + " ")
        self.searchWindowInputBox.focus()

        return

    # moves the users focus to the first item in the predicted text box
    # used to move there from the input box using the down arrow
    def moveToListBox(self, event=None):
        self.predictedTextBox.focus()
        self.predictedTextBox.select_set(0)
        return
        
    # sets main windows input box text to this windows text and removes focus from that input box
    def onDestroy(self, event=None):
        self.parent.searchInputBox.delete(0, tk.END)
        self.parent.searchInputBox.insert(0, self.searchWindowInputBoxText.get())
        self.parent.focus()
        return