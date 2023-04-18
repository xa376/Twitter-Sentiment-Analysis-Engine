import csv

# Naive Bayes Classifier, used to classify text as either positive or negative in sentiment
class SentimentAnalyzer():

    def __init__(self):
        # holds the training data, key = word, value = [negative score, positive score]
        self.wordsWithScore = {}

    # analyzes and returns the chance the word has a positive sentiment or negative sentiment
    # utilizes a naive bayes algorithm
    def analyzeWords(self, words):

        # initial probability of 50/50
        posProb = .5
        negProb = .5

        # iterates through passed words, if word has a score in the AI model, calculates that words probability and
        # multiplies it by the previous probability
        for word in words:

            if word in self.wordsWithScore:
                # probability = amount of times that word appeared in that classification / total times word appeared
                # +1 is lapace smoothing (ensures never division by 0, improves accuracy)
                posProb *= self.wordsWithScore[word][1]+1 / (self.wordsWithScore[word][0]+1 + self.wordsWithScore[word][1]+1)
                negProb *= self.wordsWithScore[word][0]+1 / (self.wordsWithScore[word][0]+1 + self.wordsWithScore[word][1]+1)

        # normalizes distribution (poschance and negchance add to 1)
        posChance = posProb / (posProb + negProb)
        negChance = negProb / (posProb + negProb)

        # returns chance is classified as positive and as negative
        return (posChance, negChance)

    # tokenizes and returns the individual words in the passed text
    def cleanText(self, text):

        # set that will store all words in the passed text
        words = set()

        # sets iterator to 0 for proceeding loop
        i = 0

        # iterates through the text, adding each word found to the set of found words, except @ mentions
        while i < len(text):

            j = i

            # initial char is the char at index i 
            char = text[i]
            
            # if current character is a letter a word is started, find the end of the word then add it
            # to the words set
            if char.isalpha():

                # word before apostrophe initially none
                beforeApos = ""

                # continues moving the right pointer until no letter is found
                # if isspace is used then . ! , after the word shows up
                while j < len(text) and (text[j].isalpha() or text[j] == "'"):

                    # if ' found then before apos will be added to next "word"
                    if text[j] == "'":
                        beforeApos = text[i:j]
                        i=j+1

                    j+=1

                # current word
                word = text[i:j]

                # If there was an apostraphe in the word adds the 2 halfs of the word
                if beforeApos != "":
                    word = beforeApos + word

                # if length of word is greater than or equal to 4 and those first 4 letters are a web link
                if len(word) >= 4 and word[:4] == "http":

                    # move cursor past web link
                    while j < len(text) and not text[j].isspace():
                        j+=1

                # if word is not empty string, add to words
                elif word:
                    words.add(word.lower())

            # iterates j to end of word to ignore @ mention
            elif char == "@":

                # move cursor past mention
                while j < len(text) and not text[j].isspace():
                    j+=1
            
            # moves left pointer to the letter after the right pointer
            i = j + 1

        # returns the set of tokenized words
        return words

    # Trains naive bayes AI model and stores it in wordsWithScore
    def train(self, fileName):

        # Reads in all training data, adding 1 to each words score in the wordsWithScore dict
        # all training data is pre-tokenized for efficiency
        with open(fileName, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                score = int(row[1])
                words = row[0].split(" ")
                for word in words:
                    if not word in self.wordsWithScore:
                        self.wordsWithScore[word] = [0, 0]
                    self.wordsWithScore[word][score] += 1

        # Reads in training test data and compares test data to trained analyzer
        correct = 0
        incorrect = 0
        with open("test_data.csv", 'r', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                posChance, negChance = self.analyzeWords(self.cleanText(row[0]))
                pred = 1 if posChance > negChance else 0
                if pred == int(row[1]):
                    correct += 1
                else:
                    incorrect += 1
        
        # Prints training results
        print(f"\nTraining complete, printing test results below.")
        print(f"Total test sentences: {correct + incorrect}")
        print(f"Correct: {correct} Incorrect {incorrect}")
        print(f"Accuracy: {round(correct / (correct + incorrect) * 100)}%\n")

        return