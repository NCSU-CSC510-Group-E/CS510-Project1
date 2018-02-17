from gensim import corpora, models, similarities
from pathlib import Path
from books import Book

def main(path_to_input, predictFile, path_to_dictionary = None, path_to_model = None,  debugging = False):

    corpus = None
    dictionary = None

    d = Path(path_to_dictionary)
    dictionaryExists = d.is_file()
    print(dictionaryExists)

    m = Path(path_to_model)
    modelExists = m.is_file()
    print(modelExists)

    # if we are given a dictionary to load, then load that instead of loading it from the corpus
    if(dictionaryExists):
        dictionary = corpora.Dictionary.load(path_to_dictionary)

    if(not modelExists):
        corpus = initializeCorpus(path_to_input, debugging)
        print(corpus)

    print(corpus)

    """
     Initialize a dictionary from our corpus
     Can't figure out why id2token isn't being populated automatically.
     Stole this inversion code from: http://code.activestate.com/recipes/252143-invert-a-dictionary-one-liner/
    """
    if(not dictionaryExists):
        dictionary = corpus.dictionary
        dictionary.save(path_to_dictionary)

    dictionary.id2token = dict([[v,k] for k,v in dictionary.token2id.items()])

    # TODO: Could also save dictionary here just for giggles

    """
     Train a model! (yay!)
     Pass in a core and a number of topics to mine for
     Providing id2word dictionary mappings here so that output of topics learned at the end are strings and not integers
    """
    if(not modelExists):
        model = models.ldamodel.LdaModel(corpus, 10, id2word = dictionary.id2token, passes=40)
        model.save(path_to_model)
    else:
        model = models.ldamodel.LdaModel.load(path_to_model)

    # TODO: Probably ought to save this model, too, just so I dont have to load it every time from scratch


    """
     Lets attempt to predict a file.
     We first need to read that file in and tokenize it
    """
    tokens = []
    with open(predictFile) as file:
        text = file.read()
        tokens = text.split()

    # tokenization
    bow = dictionary.doc2bow(tokens)

    # To make a new prediciton, just pass in a BOW vector (tokens) to test 
    # This will return array of topics + probability tuples.  
    newPrediction = model.get_document_topics(bow)

    if(debugging):
        print('Our new prediction')
        # print(newPrediction)

        for pred in newPrediction:
            print(pred)

        print('')

    # Returns the topics from the above model
    topics = model.get_topics()

    if(debugging):
        print('The topics modeled')
        print(model.print_topics(10, 5))
        print('')


def initializeCorpus(path_to_input, debugging):
    
    """"
     Need to initialize a new corpora from corpora.TextCorpus and
     initialize with lines_are_documents set to false
    """
    corpus = corpora.TextDirectoryCorpus(path_to_input, lines_are_documents=False)

    if(debugging):
        print('Dumping tokens and respective IDs')
        print(dictionary.token2id)
        print('')

        print('Dumping corpus')
        print(corpus)
        print('')

    return corpus
