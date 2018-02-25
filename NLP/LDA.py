from gensim import corpora, models

# used to determine if models exist to load from disk
from pathlib import Path

class LDA(object):
    """
    This class performs LDA on a given data set.  
    It has methods to retrive a corpus from a directory, 
    build a new model using that corpus, and to test on a given model
    """

    def __init__(self, path_to_dict = None, path_to_model = None, debugging = False):
        """
        Initialize the model we will use.
        If posisble, initialize from previous run
        """
        self.debugging = debugging
        self.path_to_dict = path_to_dict
        self.path_to_model = path_to_model

        d = Path(path_to_dict)
        dictionaryExists = d.is_file()
        if(dictionaryExists):
            self.Dictionary = corpora.Dictionary.load(path_to_dict)
        else:
            self.Dictionary = None


        m = Path(path_to_model)
        modelExists = m.is_file()

        if(modelExists):
            self.Model = models.ldamodel.LdaModel.load(path_to_model)
        else:
            self.Model = None

        self.Corpus = None
        
    def LoadCorpus(self, path_to_input):
        """"
        Need to initialize a new corpora from corpora.TextCorpus and
        initialize with lines_are_documents set to false
        """
        if(self.Dictionary == None):
            
            corpus = corpora.TextDirectoryCorpus(path_to_input, lines_are_documents=False)

            if(self.debugging):
                # print('Dumping tokens and respective IDs')
                # print(dictionary.token2id)
                # print('')

                print('Dumping corpus')
                print(corpus)
                print('')

                self.Corpus = corpus

        return self.Corpus

    def LoadDictionary(self):
        """
        """
        if(self.Dictionary == None):
            self.Dictionary = self.Corpus.dictionary

        return self.Dictionary

    def LoadModel(self, id2word, topic_count = 10, pass_count=10):
        """
        Train a model! (yay!)
        Pass in a core and a number of topics to mine for
        Providing id2word dictionary mappings here so that output of topics learned at the end are strings and not integers
        """
        if(self.Model == None):
            self.Model = models.ldamodel.LdaModel(self.Corpus, topic_count, id2word = id2word, passes=pass_count)
            self.Model.save(self.path_to_model)

        return self.Model

    def TestModel(self):
        """
        """
    
    
    

    
    
        
        
