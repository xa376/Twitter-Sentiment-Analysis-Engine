import tkinter as tk
from tkinter import ttk
from Globals import Globals as GL
from threading import Thread
from ButtonStandard import ButtonStandard
from InputWindow import InputWindow
from LabelStandard import LabelStandard
from TweetsWindow import TweetsWindow
from ClassifiedTweets import ClassifiedTweets

# the programs search menu
class SearchMenu(tk.Frame):

    def __init__(self, parent, gui):
        tk.Frame.__init__(self, parent)

        # class variable holding classifiers to use
        self.POSITIVE = "Positive"
        self.NEGATIVE = "Negative"

        # class variables to hold all tweets and their word counts
        self.classifiedTweets = ClassifiedTweets([self.POSITIVE, self.NEGATIVE])

        # configures frames grid structure for object positioning
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # displays search title
        self.title = LabelStandard(self, labelText="Search")
        self.title.grid(row=0, column=0, columnspan=2)
        
        # input box that search term will be pulled from
        self.searchInputBox = tk.Entry(self, width=64, font=GL.fontGeneral)
        self.searchInputBox.grid(sticky="w", row=1, column=0, columnspan=2, padx="12")

        # when the above input box is clicked, opens a window with an input box that utilizes predictive text
        self.searchInputBox.bind("<Button>", lambda event=None: InputWindow(self, event))

        # initializes a button that starts a search
        self.searchButton = ButtonStandard(self)
        self.searchButton.config(text="Search", width="8", command=self.prepareSearch)
        self.searchButton.grid(row=1, column=1, padx=10, sticky="e")

        # initializes a label that will be shown above the common words results of a search
        self.commonText = LabelStandard(self, labelText="Common Text")
        self.commonText.grid(row=2, column=0, columnspan=2, sticky="ne", padx=150)

        # initializes a frame the will hold the common text found in each tweet
        self.commonHolder = tk.Frame(self, height=300, width=350)
        self.commonHolder.grid(row=3, rowspan=5, column=1, columnspan=1, sticky="n", padx=10)

        # fills left side of frame with green text box, sets text to be centered, will hold common positive words
        self.commonPositive = tk.Text(self.commonHolder, font="Helvetica 16", background="#93c47d", height=12, width=15)
        self.commonPositive.tag_configure("center", justify="center")
        self.commonPositive.tag_add("center", "1.0", "end")
        self.commonPositive.insert("1.0", "POSITIVE\n\n", "center")
        self.commonPositive.pack(side="left")

        # stops user from altering positive text box
        self.commonPositive.config(state="disabled")

        # fills right side of frame with red text box, sets text to be centered, will hold common negative words
        self.commonNegative = tk.Text(self.commonHolder, font="Helvetica 16", background="#e06666", height=12, width=15)
        self.commonNegative.tag_configure("center", justify="center")
        self.commonNegative.tag_add("center", "1.0", "end")
        self.commonNegative.insert("1.0", "NEGATIVE\n\n", "center")
        self.commonNegative.pack(side="right")

        # stops user from altering negative text box
        self.commonNegative.config(state="disabled")

        # initializes a label that will display the total results of a search
        self.totalText = LabelStandard(self, labelText="Total results: ")
        self.totalText.config(width=350, font=GL.fontTweet)
        self.totalText.grid(row=3, sticky="nw", padx=100)

        # initializes a label that will display the total positive results of a search
        self.positiveText = LabelStandard(self, labelText="Positive Total: ")
        self.positiveText.grid(row=3, sticky="sw", padx=10)

        # initializes a green bar style that will be used in the following progress bar
        greenBar = ttk.Style()
        greenBar.theme_use("alt")
        greenBar.configure("green.Horizontal.TProgressbar", foreground="green", background="green")

        # initializes a green "progress bar" which will act as a visual display of the total positive tweets
        self.positiveProgress = ttk.Progressbar(self, mode="determinate", style="green.Horizontal.TProgressbar", 
                                                 orien="horizontal", length=300)
        self.positiveProgress["value"] = 0
        self.positiveProgress.grid(row=4, sticky="nw", padx=10)

        # initializes a label that will display the total negative results of a search
        self.negativeText = LabelStandard(self, labelText="Negative Total: ")
        self.negativeText.grid(row=4, sticky="sw", padx=10)

        # initializes a red bar style that will be used in the following progress bar
        redBar = ttk.Style()
        redBar.theme_use("alt")
        redBar.configure("red.Horizontal.TProgressbar", foreground="red", background="red")

        # initializes a red "progress bar" which will act as a visual display of the total negative tweets
        self.negativeProgress = ttk.Progressbar(self, mode="determinate", style="red.Horizontal.TProgressbar", 
                                                 orien="horizontal", length=300)
        self.negativeProgress["value"] = 0
        self.negativeProgress.grid(row=5, sticky="nw", padx=10)

        # Button that initializes a window to display the positive tweets
        self.positiveButton = ButtonStandard(self)
        self.positiveButton.config(text="Positive", command=lambda: TweetsWindow(gui, self.POSITIVE, self.classifiedTweets.tweets[self.POSITIVE]))
        self.positiveButton.grid(row=6, column=0, sticky="sw", padx=10, pady=10)

        # Button that initializes a window to display the negative tweets
        self.negativeButton = ButtonStandard(self)
        self.negativeButton.config(text="Negative", command=lambda: TweetsWindow(gui, self.NEGATIVE, self.classifiedTweets.tweets[self.NEGATIVE]))
        self.negativeButton.grid(row=6, column=0, sticky="sw", padx=100, pady=10)

        # makes the enter key perform a search
        self.bind("<Return>", self.prepareSearch)

    # Starts the search in a thread so current window does not become unresponsive during search
    def prepareSearch(self, event=None):
        searchThread = Thread(target=lambda: self.performSearch(event))
        searchThread.start()
        return

    # gets tweets from the twitter api, tokenizes them, classifies them, then displays results
    def performSearch(self, event=None):

        # displays searching in progress to user
        self.totalText.config(text="SEARCHING...")

        # Gets users search query from input box
        query = self.searchInputBox.get()

        # adds query to search history if not in incognito mode
        if query and not GL.incognitoMode:
            GL.searchHistory.add(query)

        # adds search settings to users query so they don't get retweets and non english tweets
        query += " -is:retweet lang:en"

        print("Getting results from twitter API...")

        # gets the tweets from the twitter api
        try:
            tweets = GL.client.search_recent_tweets(query=query, tweet_fields=["context_annotations", "created_at"], 
                                                     max_results=GL.maxResults)
        except Exception as exc:
            print("API request failure: " + str(exc))
            self.resetValues()
            return

        print("Results received successfully.")

        # if a tweet search failed, displays 0 results and resets search menu to default settings
        if not tweets.data:
            print("No results found.")
            self.resetValues()
            return

        # clears results of previous search
        self.classifiedTweets.clear()

        # common meaningless words, wont be shown in common words text boxes
        meaninglessWords = set(["a", "the", "and", "i", "is"])

        # cleans tweet, classifies tweet, adds tweet to applicable list, adds each word in tweet
        # to applicable word dictionary
        for tweet in tweets.data:
            words = GL.sentimentAnalyzer.cleanText(tweet.text)
            posChance, negChance = GL.sentimentAnalyzer.analyzeWords(words)

            # assumes negative if equal probability
            if posChance > negChance:
                self.classifiedTweets.tweets[self.POSITIVE].append(tweet.text)
                for word in words:
                    if not word in meaninglessWords:
                        if not word in self.classifiedTweets.wordsCount[self.POSITIVE].keys():
                            self.classifiedTweets.wordsCount[self.POSITIVE][word] = 0
                        self.classifiedTweets.wordsCount[self.POSITIVE][word] += 1
            else:
                self.classifiedTweets.tweets[self.NEGATIVE].append(tweet.text)
                for word in words:
                    if not word in meaninglessWords:
                        if not word in self.classifiedTweets.wordsCount[self.NEGATIVE].keys():
                            self.classifiedTweets.wordsCount[self.NEGATIVE][word] = 0
                        self.classifiedTweets.wordsCount[self.NEGATIVE][word] += 1

        # holds totals of each classification (which is equal to the tweets list length)
        positiveTotal = self.classifiedTweets.getTotal(self.POSITIVE)
        negativeTotal = self.classifiedTweets.getTotal(self.NEGATIVE)

        # sets each progress bar to its classifications percent of the total tweets
        self.positiveProgress["value"] = (positiveTotal / (positiveTotal + negativeTotal)) * 100
        self.negativeProgress["value"] = (negativeTotal / (positiveTotal + negativeTotal)) * 100

        # sets totals texts to tweet totals
        self.positiveText.config(text="Positive Total: " + str(positiveTotal))
        self.negativeText.config(text="Negative Total: " + str(negativeTotal))
        self.totalText.config(text="Total results: " + str(positiveTotal + negativeTotal))

        # inserts each positive word into the common positive box, sorted by occurance (high to low)
        self.commonPositive.config(state="normal")
        self.commonPositive.delete("0.0", tk.END)
        self.commonPositive.insert("1.0", "POSITIVE\n\n", "center")
        for word, count in sorted(self.classifiedTweets.wordsCount[self.POSITIVE].items(), key=lambda _:_[1], reverse=True):
            self.commonPositive.insert(tk.END, word + " x" + str(count) + "\n\n")

        # stops user from altering text box
        self.commonPositive.config(state="disabled")
        
        # inserts each negative word into the common negative box, sorted by occurance (high to low)
        self.commonNegative.config(state="normal")
        self.commonNegative.delete("0.0", tk.END)
        self.commonNegative.insert("1.0", "NEGATIVE\n\n", "center")
        for word, count in sorted(self.classifiedTweets.wordsCount[self.NEGATIVE].items(), key=lambda _:_[1], reverse=True):
            self.commonNegative.insert(tk.END, word + " x" + str(count) + "\n\n")

        # stops user from altering text box
        self.commonNegative.config(state="disabled")

        return

    # resets search menu to default values and 0 results
    def resetValues(self):

        self.totalText.config(text="Total Results: 0")
        self.positiveText.config(text="Positive Total: ")
        self.negativeText.config(text="Negative Total: ")
        self.positiveProgress["value"] = 0
        self.negativeProgress["value"] = 0

        self.commonPositive.config(state="normal")
        self.commonPositive.delete("0.0", tk.END)
        self.commonPositive.insert("1.0", "POSITIVE\n\n", "center")
        self.commonPositive.config(state="disabled")

        self.commonNegative.config(state="normal")
        self.commonNegative.delete("0.0", tk.END)
        self.commonNegative.insert("1.0", "NEGATIVE\n\n", "center")
        self.commonNegative.config(state="disabled")

        self.classifiedTweets.clear()

        return