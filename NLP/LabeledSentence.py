"""
Gensim Doc2Vec needs model training data in an LabeledSentence iterator object
modified to iterate through documents instead of a list
"""

class LabeledLineSentence(object):
    def __init__(self, docData, docLabels):
        """
        docLabels = the labels list for the documents (filenames)
        docData = the raw contents list of the documents 
        """
       self.docLabels = docLabels
       self.docData = docData
    def __iter__(self):
        for idx, doc in enumerate(self.docData):
            #split because the model is trained on a word-to-word basis
            #could possibly tokenize here to get rid of common words
            yield LabeledSentence(words=doc.split(),labels=[self.docLabels[idx]])