from gensim import corpora, models, similarities

def main(path_to_input, debugging = False):
    # Each element in array is considered one "document"
    documents = ["Human machine interface for lab abc computer applications",
                "A survey of user opinion of computer system response time",
                "The EPS user interface management system",
                "System and human system engineering testing of EPS",
                "Relation of user perceived response time to error measurement",
                "The generation of random binary unordered trees",
                "The intersection graph of paths in trees",
                "Graph minors IV Widths of trees and well quasi ordering",
                "Graph minors A survey"]

    # Need to initialize a new corpora from corpora.TextCorpus and initialize with lines_are_documents set to false

    corpus = corpora.TextDirectoryCorpus('input/', lines_are_documents=False)

    dictionary = corpus.dictionary
    # Can save w/ dictionary.save()

    if(debugging):
        print('Dumping tokens and respective IDs')
        print(dictionary.token2id)
        print('')

        print('Dumping corpus')
        print(corpus)
        print('')


    # Can't figure out why id2token isn't being populated automatically.
    # Stole this inversion code from: http://code.activestate.com/recipes/252143-invert-a-dictionary-one-liner/
    dictionary.id2token = dict([[v,k] for k,v in dictionary.token2id.items()])

    # TODO: Could also save dictionary here just for giggles


    # Pass in a core and a number of topics to mine for
    # TODO: Probably ought to save this model, too, just so I dont have to load it every time from scratch
    model = models.ldamodel.LdaModel(corpus, 10, id2word = dictionary.id2token, passes=40)


    # To make a new prediciton, just pass in a BOW vector to test 
    # This will return array of topics + probability tuples.  
    newPrediction = model.get_document_topics([(8, 1.0), (10, 1.0), (11, 1.0)])

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
        print(model.print_topics(3, 2))
        print('')
