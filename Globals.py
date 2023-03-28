import tweepy
from CustomTrie import Trie
from TrieNode import Node
from SentimentAnalyzer import SentimentAnalyzer
import os.path

# holds all global variables for the program
class Globals():

    # Logs into twitter client
    if os.path.exists("./login.txt"):
        with open("login.txt", 'r') as file:
            token = file.readline()
        client = tweepy.Client(bearer_token=token)
    else:
        print("No bearer token found.")

    # Holds users search history
    searchHistory = set()

    # default color scheme (dark)
    backgroundColor = "#444444"
    foregroundColor = "#eeeeee"
    activeBackgroundColor = "#1a1a1a"
    activeForegroundColor = "#ffffff"
    listSelectedColor = "#797979"

    # default font values
    fontLarge = "Helvetica 20"
    fontGeneral = "Helvetica 12"
    fontTweet = "Helvetica 10"

    # default button border
    buttonBorder = "ridge"

    # trie data structure that will hold all words for predictive text
    allWords = Trie()

    # stores Naive Bayes AI model
    sentimentAnalyzer = SentimentAnalyzer()

    # max results to request from the api during a search
    maxResults = 10

    # search history saved if false, else search history not saved
    incognitoMode = False

    # turns true when startup tasks are finished, loading screen uses this message to close
    finishedLoading = False