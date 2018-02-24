from gensim import corpora, models
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

        d = Path(path_to_dictionary)
        dictionaryExists = d.is_file()
        if(dictionaryExists):
            self.Dictionary = corpora.Dictionary.load(path_to_dict)
        else:
            self.Dictionary = None


        m = Path(path_to_model)
        modelExists = m.is_file()

        if(modelExists):
            self.model = models.ldamodel.LdaMode.load(path_to_model)
        else:
            self.Model = None

        self.Corpus = None
        
    def LoadCorpus(path_to_input):
        """
        """
        if(self.Corpus == None):
            
        """"
        Need to initialize a new corpora from corpora.TextCorpus and
        initialize with lines_are_documents set to false
        """
        corpus = corpora.TextDirectoryCorpus(path_to_input, lines_are_documents=False)

        if(self.debugging):
            # print('Dumping tokens and respective IDs')
            # print(dictionary.token2id)
            # print('')

            print('Dumping corpus')
            print(corpus)
            print('')

        return corpus

    def LoadDictionary():
        """
        """

    def LoadModel():
        """
        """

    def TestModel():
        """
        """
    
    
    

    
    
        
        
