from Globals import Globals as GL
from GUI import GUI
import os.path
from threading import Thread
from LoadingScreen import LoadingScreen
import time
import pickle
import tweepy

def main():

    # holds time for startup time counter
    start = time.perf_counter()

    print("Performing program startup...\n")

    # creates and starts a thread for the loading screen so that that startup tasks can continue
    # while the loading screen loop is running
    loadingThread = Thread(target=displayLoadingScreen)
    loadingThread.start()

    # startup tasks to load settings, search history, build the trie predictive text model,
    # and train the naive bayes sentiment analysis model
    connectTwitter()
    readSettings()
    readSearchHistory()
    loadTrie()
    loadAnalyzer()

    # Will trigger the loading screen thread to close now that startup tasks are finished
    GL.finishedLoading = True

    # rejoins the threads
    loadingThread.join()

    # holds time that startup finished
    finish = time.perf_counter()

    # displays startup time
    print(f"\nStartup completed in: {round(finish-start, 2)}s\n")

    # initializes and starts the programs user interface
    gui = GUI()
    gui.mainloop()

    print("Saving setup files...")

    # saves the users search history and settings in the local file directory
    writeSearchHistory()
    writeSettings()

    print("User setup files saved successfully.")

# Logs into twitter client
def connectTwitter():

    # Reads bearer token from login file and connects to API
    if os.path.exists("./login.txt"):
        with open("login.txt", 'r') as file:
            token = file.readline()
        GL.client = tweepy.Client(bearer_token=token)
    else:
        print("No bearer token found.")

    return

# Attempts to load a SentimentAnalyzer object, creates and trains one if not found
def loadAnalyzer():

    # Loads SentimentAnalyzer
    if os.path.exists("./analyzer.pickle"):
        print("Analyzer file found, loading analyzer...")
        with open("analyzer.pickle", "rb") as analyzer:
            GL.sentimentAnalyzer = pickle.load(analyzer)
    # Trains SentimentAnalyzer
    elif os.path.exists("./training_data.csv"):
        print("Analyzer file not found, training new analyzer...")
        GL.sentimentAnalyzer.train("training_data.csv")
        with open("analyzer.pickle", "wb") as analyzer:
            pickle.dump(GL.sentimentAnalyzer, analyzer, protocol=pickle.HIGHEST_PROTOCOL)
    # No pretrained analyzer or training files found
    else:
        print("Analyzer and training files not found, please redownload the associated files to implement this feature.")

    print("Analyzer setup completed.")
    return

# displays a loading screen until the finishedLoading variable is set to true
def displayLoadingScreen():
    loadingScreen = LoadingScreen()
    loadingScreen.mainloop()
    return

# Writes users settings to a settings file, new line deliminated
def writeSettings():
    with open("settings.txt", 'w') as file:
        file.write(str(GL.maxResults) + "\n" + str(GL.incognitoMode))
    return

# Reads users settings from a settings file and sets those settings
def readSettings():

    if os.path.exists("./settings.txt"):
        with open("settings.txt", 'r') as file:
            lines = file.read().splitlines()
            GL.maxResults = int(lines[0])
            GL.incognitoMode = (lines[1] == "True")
        print("Settings file loaded successfully.")
    else:
        print("Settings file not found.")

    return

# builds the allWords trie using a txt file containing all english words
def loadTrie():

    # Loads the Trie object if it exists
    if os.path.exists("./prediction.pickle"):
        print("Text prediction file found, loading prediction object...")
        with open("prediction.pickle", "rb") as prediction:
            GL.allWords = pickle.load(prediction)
    # Trains the Trie object
    elif os.path.exists("./words.txt"):
        print("Text prediction file not found, creating new prediction object...")
        with open("words.txt", 'r') as file:
            for line in file.read().splitlines():
                GL.allWords.insert(line)
        with open("prediction.pickle", "wb") as prediction:
            pickle.dump(GL.allWords, prediction, protocol=pickle.HIGHEST_PROTOCOL)
    # No Trie object found
    else:
        print("No text prediction files found. Please redownload.")

    print("Text prediction setup completed.")
    return

# reads a users search history into the search history set
def readSearchHistory():
    if os.path.exists("./history.txt"):
        with open("history.txt", 'r') as file:
            for line in file.read().splitlines():
                GL.searchHistory.add(line)
        print("History file loaded successfully.")
    else:
        print("History file not found.")
    return

# writes the users search history into a history txt file in the program file directory
def writeSearchHistory():
    with open("history.txt", 'w') as file:
        for line in GL.searchHistory:
            file.write(line + "\n")
    return

# Python best practice
if __name__ == "__main__":
    main()