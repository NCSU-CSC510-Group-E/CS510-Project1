"""
Gensim Doc2Vec needs model training data in an iterator object
- modified to iterate through documents instead of a list
"""
from gensim.models import doc2vec

#this was depreciated need to use TaggedBrownCorpus ?



class TaggedDocs(object):
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
            
            yield doc2vec.TaggedDocument(words=doc.split(),tags=[self.docLabels[idx]])


    ## With the current gensim implementation, all label vectors are stored separately in RAM.
    ## they report being able to run 2 million different sentences no problem, however