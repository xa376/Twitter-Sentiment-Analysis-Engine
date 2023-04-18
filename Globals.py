from CustomTrie import Trie
from SentimentAnalyzer import SentimentAnalyzer

# holds all global variables for the program
class Globals():

    # Twitter client used to communicate with API
    client = None
    
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