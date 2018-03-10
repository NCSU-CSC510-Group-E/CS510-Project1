# Our similarity measures
from gensim.matutils import jaccard
from gensim.matutils import cossim
import pprint
# used to determine if models exist to load from disk
from pathlib import Path

# Used to read files from disk
import os

from NLP_models.LDA import LDA

# Our ORM
from DB_models.books import Book

def main(path_to_training_data, path_to_test_data, path_to_dictionary = None, path_to_model = None,  debugging = False):

    lda = LDA(path_to_dictionary, path_to_model, debugging)

    corpus = lda.LoadCorpus(path_to_training_data + 'body/')

    dictionary = lda.LoadDictionary()

    dictionary.id2token = dict([[v,k] for k,v in dictionary.token2id.items()])

    model = lda.LoadModel(dictionary.id2token)
    # after train the model, print out each topics
    print('------Top 10 words in each topic--------')
    pprint.pprint(model.show_topics())
    
    """
     Lets attempt to predict our files.
     We first need to read that file in and tokenize it
    """
    print('-----------Test the model---------------')
    predictFiles(path_to_test_data, model, dictionary, debugging)


 
# TODO: This needs to be refactored so the meat of the prediction work is being done inside my fancy LDA class
def predictFiles(path_to_test_data, model, dictionary, debugging):
    path_to_test_labels = path_to_test_data + 'tags/'
    path_to_test_data = path_to_test_data + 'body/'
    
    files = os.listdir(path_to_test_data)
    likelihoods = []
    jaccards = []
    cossims = []
    for file in files:
        # skip pesky dotfiles (thanks OSX with your .DS_STORE 
        if(file[0] == '.'):
            continue

        if(debugging):
            print('Reading file {}'.format(path_to_test_data + file))

        tokens = []
        with(open(path_to_test_data + file)) as f:
            text = f.read()
            tokens = text.split()
        with(open(path_to_test_labels + file)) as f:
            text = f.read()
            labels = text.split(',')

        # This is where we will need to read in the vector of tags
        # We will need to set the "likelihood" of each of those terms to 100%.

        # tokenization
        bow = dictionary.doc2bow(tokens)
        labels = dictionary.doc2bow(labels)

        # To make a new prediciton, just pass in a BOW vector (tokens) to test 
        # This will return array of topics + probability tuples.  
        newPrediction = model.get_document_topics(bow, minimum_probability=.1)

        # Returns the topics from the above model
        topics = model.get_topics()
        if(debugging):
            print('The topics modeled in file: {}'.format(file))
            print('There are {} predicted topics, here is the max likelihood one:'.format(len(newPrediction)))
            newPrediction.sort(key=lambda tup: tup[1])
            pred = newPrediction[0]

            topic_id = pred[0]
            Likelihood = pred[1]
            topic_word = []
            for i in range(10):
                topic_word.append(model.show_topic(topic_id)[i][0])
            topic_bow = dictionary.doc2bow(topic_word)

                #here, we need to calculate the similarity of topics found to the tags vector
            jac = jaccard(topic_bow, labels)
            cos = cossim(topic_bow, labels)

            print('Topic: {}, Likelihood:{}, \nJacc: {}, \tCos: {}\n'.format(topic_id, Likelihood, jac, cos))

            print('')

            likelihoods.append(Likelihood)
            jaccards.append(jac)
            cossims.append(cos)
    print('---------Final average results for {} test files--------'.format(len(files)))
    print('Likelihood: {}'.format(sum(likelihoods)/len(likelihoods)))
    print('Jacc: {}'.format(sum(jaccards)/len(jaccards)))
    print('Cos: {}'.format(sum(cossims)/len(cossims)))

        # if(debugging):
        #     print('The topics modeled in file: {}'.format(file))
        #     for pred in newPrediction:

        #         topicTerms = model.get_topic_terms(pred[0], topn=5 )


        #         #here, we need to calculate the similarity of topics found to the tags vector
        #         jac = jaccard(topicTerms, labels)
        #         cos = cossim(topicTerms, labels)

        #         print('Topic: {}, Likelihood:{}, \nJacc: {}, \tCos: {}\n'.format(pred[0], pred[1], jac, cos))

        #         for (key, val) in enumerate(topicTerms):
        #             print('\tWord:{} , \tLikelihood: {}'.format(dictionary.id2token[key], val[1]))
        #     print('')