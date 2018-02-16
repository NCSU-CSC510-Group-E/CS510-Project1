from gensim import corpora, models, similarities

def main(path_to_input, predictFile, debugging = False):
    # Need to initialize a new corpora from corpora.TextCorpus and initialize with lines_are_documents set to false
    corpus = corpora.TextDirectoryCorpus(path_to_input, lines_are_documents=False)

    # if we are given a dictionary to load, then load that instead of loading it from the corpus
    if(path_to_dictionary is not None):
        dictionary = corpora.Dictionary.load(path_to_dictionary)



    # Can't figure out why id2token isn't being populated automatically.
    # Stole this inversion code from: http://code.activestate.com/recipes/252143-invert-a-dictionary-one-liner/
    dictionary.id2token = dict([[v,k] for k,v in dictionary.token2id.items()])

    # TODO: Could also save dictionary here just for giggles

    # Pass in a core and a number of topics to mine for
    # TODO: Probably ought to save this model, too, just so I dont have to load it every time from scratch
    # Providing id2word dictionary mappings here so that output of topics learned at the end are strings and not integers
    model = models.ldamodel.LdaModel(corpus, 10, id2word = dictionary.id2token, passes=40)


    # Lets attempt to predict a file.
    # We first need to read that file in and tokenize it
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
