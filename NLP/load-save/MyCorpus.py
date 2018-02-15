from gensim import corpora
from six import iteritems #for creating dictionary

class MyCorpus():
    def __init__(self, documentFile='input.txt', load=False, loadFile='dictionary.dict'):
        self._doc = documentFile

        if load:
            self._dict = self.loadDict(loadFile)
        else:
            self._dict = self.createDict()

    #yield vector for each docment one at a time
    def __iter__(self):
        for line in open(self._doc):
            # assume there's one document per line, tokens separated by whitespace
            yield self._dict.doc2bow(line.lower().split())

    """
    save dictionary for later use
    """
    def saveDict(self, fileName='dictionary'):
        self._dict.save(fileName + ".dict")


    """
    load a dictionary
    """
    def loadDict(self, fileName):
        return corpora.Dictionary.load(fileName)

    """
    create the dictionary of tokenized bag-of-words
    """
    def createDict(self):

        stoplist = set('for a of the and to in'.split())

        # collect statistics about all tokens
        dictionary = corpora.Dictionary(line.lower().split() for line in open(self._doc))
        # remove stop words and words that appear only once
        stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
                    if stopword in dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
        dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
        dictionary.compactify()  # remove gaps in id sequence after words that were removed

        return dictionary


