# Node for a trie data structure
class Node():

    def __init__(self, char):
        self.val = char
        self.isWord = False
        self.children = {}