import tkinter as tk
from tkinter import ttk
from Globals import Globals as GL
from MainMenu import MainMenu
from SearchMenu import SearchMenu
from HistoryMenu import HistoryMenu
from SettingsMenu import SettingsMenu

# Main program window, contains MainMenu, SearchMenu, HistoryMenu, SettingsMenu, and
# allows for switching between them
class GUI(tk.Tk):

    def __init__(self):
        super().__init__()

        # Window title
        self.title("Twitter Sentiment Analysis Engine")

        # window size settings
        windowWidth = 700
        windowHeight = 400

        # users current screen size
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        # offset variables used when setting window geometry to make window center
        x = int((screenWidth/2) - (windowWidth/2))
        y = int((screenHeight/2) - (windowHeight/2))

        # Sets the window to be windowWidth x windowHeight, opening in screen center
        self.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

        # makes window fixed size
        self.resizable(False, False)

        # this is the main frame that will contain MainMenu, SearchMenu, HistoryMenu, SettingsMenu (fills window)
        box = ttk.Frame(self)
        box.pack(side="top", fill="both", expand=True)
        box.grid_rowconfigure(0, weight=1)
        box.grid_columnconfigure(0, weight=1)

        # creates a menubar in the main frame
        menubar = tk.Menu(box)
        
        # Adds File Menu and all file menu options, each options frame is shown if pressed
        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file)
        file.add_command(label='Home', command=lambda: self.showFrame(MainMenu))
        file.add_command(label='Search', command=lambda: self.showFrame(SearchMenu))
        file.add_command(label='History', command=lambda: self.showFrame(HistoryMenu))
        file.add_command(label='Settings', command=lambda: self.showFrame(SettingsMenu))
        file.add_separator()
        file.add_command(label='Close', command=self.destroy)
        self.config(menu=menubar)

        # Dictionary that will hold all of the window frames
        self.frames = {}
        
        # Initializes all frames and stores them in frames dictionary
        for currentFrame in (MainMenu, SearchMenu, HistoryMenu, SettingsMenu):

            # Initializes a frame with this windows box frame as its parent
            frame = currentFrame(box, self)

            # Stores the frame in the frames dictionary
            self.frames[currentFrame] = frame

            # Makes frame fill its space and sets the background color
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg=GL.backgroundColor)

        # brings window to front, otherwise window opens behind other program windows
        self.lift()
        self.attributes('-topmost',True)
        self.after_idle(self.attributes,'-topmost',False)

        # window initially shows the main menu
        self.showFrame(MainMenu)

    # displays the passed frame
    def showFrame(self, currentFrame):

        frame = self.frames[currentFrame]

        # updates history menu with any new searches before displaying 
        if currentFrame == HistoryMenu:
            frame.updateHistory()

        # sets users focus to the frame
        frame.tkraise()
        frame.focus()