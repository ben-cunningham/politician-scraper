from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

if __name__ == '__main__':
    train = []
    cl = NaiveBayesClassifier(train)
    cl.classify("")
