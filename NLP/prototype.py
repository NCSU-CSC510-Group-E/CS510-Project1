from gensim import corpora, models, similarities

# A core of 9 documents, each consisting of some number of words
corpus = [[(0, 1.0), (1, 1.0), (2, 1.0)],
           [(2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (8, 1.0)],
           [(1, 1.0), (3, 1.0), (4, 1.0), (7, 1.0)],
           [(0, 1.0), (4, 2.0), (7, 1.0)],
           [(3, 1.0), (5, 1.0), (6, 1.0)],
           [(9, 1.0)],
           [(9, 1.0), (10, 1.0)],
           [(9, 1.0), (10, 1.0), (11, 1.0)],
           [(8, 1.0), (10, 1.0), (11, 1.0)]]


# Pass in a core and a number of topics to mine for
model = models.ldamodel.LdaModel(corpus, 10)


# To make a new prediciton, just pass in a vector to test 
newPrediction = model[[(8, 1.0), (10, 1.0), (11, 1.0)]]

print(newPrediction)
