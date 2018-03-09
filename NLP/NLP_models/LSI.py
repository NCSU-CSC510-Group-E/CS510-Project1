


from gensim.test.utils import common_dictionary, common_corpus
from gensim.models import LsiModel
from gensim import corpora, models
from textcorpusOEM import TextDirectoryCorpus
import os
def predictFiles(path_to_test_data, model, dictionary, debugging):
    path_to_test_labels = path_to_test_data + 'tags/'
    path_to_test_data = path_to_test_data + 'body/'
    
    files = os.listdir(path_to_test_data)
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
            for pred in newPrediction:

                topicTerms = model.get_topic_terms(pred[0], topn=5 )


                #here, we need to calculate the similarity of topics found to the tags vector
                jac = jaccard(topicTerms, labels)
                cos = cossim(topicTerms, labels)

                print('Topic: {}, Likelihood:{}, \nJacc: {}, \tCos: {}\n'.format(pred[0], pred[1], jac, cos))

                for (key, val) in enumerate(topicTerms):
                    print('\tWord:{} , \tLikelihood: {}'.format(dictionary.id2token[key], val[1]))
            print('')

#Biuld corpus and dictionay
path_to_input = '/Users/zhangqi/Documents/CS510-Project1/NLP/soFileTrain/'
corpus = TextDirectoryCorpus(path_to_input, lines_are_documents=False)
Dictionary = corpus.dictionary
Dictionary.id2token = dict([[v,k] for k,v in Dictionary.token2id.items()])

#training our lsi model based on corpus            
model = LsiModel(corpus)
model.get_topics()
model.print_topics()
print(corpus)
print('we are done')
# vectorized_corpus = model[common_corpus]  # vectorize input copus in BoW format

# predictFiles('/Users/zhangqi/Documents/CS510-Project1/NLP/soFileTest/', model, Dictionary,True)
# TODO: This needs to be refactored so the meat of the prediction work is being done inside my fancy LDA class
