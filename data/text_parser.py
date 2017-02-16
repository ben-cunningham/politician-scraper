from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

class TextParser():
    
    def __init__(self):
        train = []

        self.cl = NaiveBayesClassifier(train)

    def classify(string):
        return cl.classify(string)
