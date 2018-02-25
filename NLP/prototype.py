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

    lda = LDA(path_to_dictionary, path_to_model)

    corpus = lda.LoadCorpus(path_to_training_data)

    dictionary = lda.Dictionary

    dictionary.id2token = dict([[v,k] for k,v in dictionary.token2id.items()])

    model = lda.LoadModel(dictionary.id2token)

    """
     Lets attempt to predict our files.
     We first need to read that file in and tokenize it
    """
    predictFiles(path_to_test_data, model, dictionary, debugging)



def predictFiles(path_to_test_data, model, dictionary, debugging):
    path_to_test_data = path_to_test_data + '/body/'
    path_to_test_labels = path_to_test_data + '/tags/'
    
    files = os.listdir(path_to_test_data)
    for file in files:
        if(debugging):
            print('Reading file {}'.format(path_to_test_data + file))

        tokens = []
        with(open(path_to_test_data + file)) as f:
            text = f.read()
            tokens = text.split()
        with(open(path_to_test_labels)) as f:
            text = f.read()
            labels = text.split(',')

        # This is where we will need to read in the vector of tags
        # We will need to set the "likelihood" of each of those terms to 100%.

        # tokenization
        bow = dictionary.doc2bow(tokens)
        labels = dictionary.doc2bow(labels)

        # To make a new prediciton, just pass in a BOW vector (tokens) to test 
        # This will return array of topics + probability tuples.  
        newPrediction = model.get_document_topics(bow, minimum_probability=.5)

        # Returns the topics from the above model
        topics = model.get_topics()

        if(debugging):
            print('The topics modeled in file: {}'.format(file))
            for pred in newPrediction:
                print('Topic: {}, {} Likelihood'.format(pred[0], pred[1]))

                topicsFound = model.get_topic_terms(pred[0], topn=2 )

                jac = jaccard(topicsFound, labels)
                cos = cossim(topicsFound, labels)



                #here, we need to calculate the similarity of topics found to the tags vector

                print(topicsFound)

                # for (key, val) in enumerate(topicsFound):
                #     print('\tWord:{} , \tLikelihood: {}'.format(dictionary.id2token[key], val[1]))
                #     # print(val)


            print('')
