"""
Gensim Doc2Vec needs model training data in an LabeledSentence iterator object
modified to iterate through documents instead of a list
"""

class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield LabeledSentence(words=doc.split(),labels=[self.labels_list[idx]])