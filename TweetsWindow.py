import tkinter as tk
from tkinter import ttk
from Globals import Globals as GL
from LabelStandard import LabelStandard
from ButtonStandard import ButtonStandard

# window that displays passed tweets with a passed classifier
class TweetsWindow(tk.Toplevel):

    def __init__(self, parent, tweetClass="None", tweets=[]):
        tk.Toplevel.__init__(self, parent)

        # sets parents window and name of the tweet classifier
        self.parent = parent
        self.tweetClass = tweetClass

        # sets window styling
        self.config(background=GL.backgroundColor)

        # makes window size fixed
        self.resizable(False, False)

        # Makes parent window untouchable (user can only interact with this one)
        self.grab_set()

        # sets title
        self.title(tweetClass)
        title = LabelStandard(self, labelText=tweetClass + " Tweets")
        title.config(font=GL.fontTweet)
        title.pack()

        # frame that will hold the tweet display box and its scrollbar
        messageFrame = ttk.Frame(self, width="100", height="100")
        messageFrame.pack()

        # scroll bar for the tweet display box
        scrollBar = tk.Scrollbar(messageFrame, orient="vertical")
        scrollBar.pack(side="right", fill="y")

        # box that the tweets will be displayed in
        tweetDisplayBox = tk.Text(messageFrame, width="80", height="15", font=GL.fontTweet, 
                                  background=GL.activeBackgroundColor, foreground=GL.foregroundColor, yscrollcommand=scrollBar.set)
        tweetDisplayBox.pack()

        # makes the "center" take center text
        tweetDisplayBox.tag_configure("center", justify="center")

        # iterates through each tweet, displaying the current tweet number on one line, and the tweet on the next
        for i, tweet in enumerate(tweets):
            tweetDisplayBox.insert(tk.END, ("-"*35) + " Tweet " + str(i+1) + " " + ("-"*35), "center")
            tweetDisplayBox.insert(tk.END, "\n" + tweet + "\n\n")

        # makes tweets uneditable by user (needs to happen AFTER finished inserting)
        tweetDisplayBox.config(state="disabled")

        # enables scrollbar for tweet display box use
        scrollBar.config(command=tweetDisplayBox.yview)

        # button that closes the window when pressed
        okButton = ButtonStandard(self)
        okButton.config(text="OK", width=5, font=GL.fontTweet, command=self.destroy)
        okButton.pack()

        # closes window when enter is pressed
        self.bind("<Return>", func=lambda event=None: self.destroy())
        
        # sets the users focus to the window after its displayed
        self.after(1, self.focus)