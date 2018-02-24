# Models used for analysis
from gensim import corpora, models, similarities

# Our similarity measures
from gensim.matutils import jaccard
from gensim.matutils import cossim

# used to determine if models exist to load from disk
from pathlib import Path

# Our ORM
from books import Book

# Used to read files from disk
import os

from LDA import LDA

def main(path_to_training_data, path_to_test_data, path_to_dictionary = None, path_to_model = None,  debugging = False):

    path_to_test_data = path_to_test_data + '/'
    corpus = None
    dictionary = None

    d = Path(path_to_dictionary)
    dictionaryExists = d.is_file()

    m = Path(path_to_model)
    modelExists = m.is_file()

    # if we are given a dictionary to load, then load that instead of loading it from the corpus
    if(dictionaryExists):
        dictionary = corpora.Dictionary.load(path_to_dictionary)

    if(not modelExists):
        corpus = initializeCorpus(path_to_training_data, debugging)
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

    """
     Lets attempt to predict our files.
     We first need to read that file in and tokenize it
    """
    predictFiles(path_to_test_data, model, dictionary, debugging)


def initializeCorpus(path_to_training_data, debugging):
    
    """"
     Need to initialize a new corpora from corpora.TextCorpus and
     initialize with lines_are_documents set to false
    """
    corpus = corpora.TextDirectoryCorpus(path_to_training_data, lines_are_documents=False)

    if(debugging):
        # print('Dumping tokens and respective IDs')
        # print(dictionary.token2id)
        # print('')

        print('Dumping corpus')
        print(corpus)
        print('')

    return corpus


def predictFiles(path_to_test_data, model, dictionary, debugging):
    
    files = os.listdir(path_to_test_data)
    for file in files:
        if(debugging):
            print('Reading file {}'.format(path_to_test_data + file))

        tokens = []
        with(open(path_to_test_data + file)) as f:
            text = f.read()
            tokens = text.split()

        # This is where we will need to read in the vector of tags
        # We will need to set the "likelihood" of each of those terms to 100%.

        # tokenization
        bow = dictionary.doc2bow(tokens)

        # To make a new prediciton, just pass in a BOW vector (tokens) to test 
        # This will return array of topics + probability tuples.  
        newPrediction = model.get_document_topics(bow, minimum_probability=.1)

        # Returns the topics from the above model
        topics = model.get_topics()

        if(debugging):
            print('The topics modeled in file: {}'.format(file))
            for pred in newPrediction:
                print('Topic: {}, {} Likelihood'.format(pred[0], pred[1]))

                topicsFound = model.get_topic_terms(pred[0], topn=2 )

                #here, we need to calculate the similarity of topics found to the tags vector

                for (key, val) in enumerate(topicsFound):
                    print('\tWord:{} , \tLikelihood: {}'.format(dictionary.id2token[key], val[1]))
                    # print(val)


            print('')
