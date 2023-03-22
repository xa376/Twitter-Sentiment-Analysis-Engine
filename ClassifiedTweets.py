# holds all tweets after they are classified
class ClassifiedTweets():

    def __init__(self, classifiers):

        # stores each tweet with the given classification, key= classifier | value= raw tweet
        self.tweets = {}
        # stores sets of words with the given classification, key= classifier | value= dict{word : word count}
        self.wordsCount = {}

        # fills the data structures with classifier keys with empty values
        for classifier in classifiers:
            self.tweets[classifier] = []
            self.wordsCount[classifier] = {}

    # returns the total amount of results of a given classifier
    def getTotal(self, classifier):
        return len(self.tweets[classifier])
    
    # clears the stored tweets and word counts
    def clear(self):
        for key in self.tweets.keys():
            self.tweets[key] = []
        for key in self.wordsCount.keys():
            self.wordsCount[key] = {}