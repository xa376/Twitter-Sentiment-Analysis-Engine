from TrieNode import Node

# Trie data structure for word prediction
class Trie():

    def __init__(self):
        self.root = Node("")

    # inserts a word into the data structure, setting the last nodes isWord attribute to True
    def insert(self, word):
        
        # sets current node to root
        node = self.root

        # for each character if the current node has a node with that char as a child, moves to it,
        # else inserts a new node of that char as the current nodes child, then moves to it
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                newNode = Node(char)
                node.children[char] = newNode
                node = newNode
        
        # ending node is last char in word, so set isWord to true
        node.isWord = True

    # returns a collection of predictedWords
    def predict(self, prefix):

        # max words to put in predictedWords, increasing reduces performance
        MAX_VALUES = 10

        # initial empty set
        predictedWords = set()

        # sets current node to root
        node = self.root

        # if no word prefix was passed then nothing to predict
        if not prefix:
            return predictedWords

        # moves from root node to last char node in prefix
        for char in prefix:

            # if there are no suggestions to make leaves function
            if not char in node.children.keys():
                return predictedWords

            # sets current node to the last prefix character
            node = node.children[char]

        # creates a queue for BFS through Trie
        queue = []

        # initial queue is the children of the prefix's last char node
        # because setting to last char node includes the inital prefix in predictedWords collection
        for char, child in node.children.items():
            queue.append((child, prefix + char))

        # while theres a queue and the max values to put in predicted words is not reached
        # add words to predicted words
        while queue and len(predictedWords) < MAX_VALUES:

            # remove next node/prefix from queue
            node, prefix = queue.pop(0)

            # if the node is a word add the prefix to the queue
            if node.isWord:
                predictedWords.add(prefix)
            
            # add this nodes children to the back of the queue, adding the nodes char to the prefix
            for char, child in node.children.items():
                queue.append((child, prefix + char))

        return predictedWords