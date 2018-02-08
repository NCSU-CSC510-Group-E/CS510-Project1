from gensim import corpora, models, similarities

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

# Build an array where each element is a document
# and each document is an array of words
texts = [[word for word in document.lower().split()]
          for document in documents]

dictionary = corpora.Dictionary(texts)
# Can save w/ dictionary.save()

corpus = [dictionary.doc2bow(text) for text in texts]
# Could also save here just for giggles

# Pass in a core and a number of topics to mine for
model = models.ldamodel.LdaModel(corpus, 10)


# To make a new prediciton, just pass in a vector to test 
newPrediction = model[[(8, 1.0), (10, 1.0), (11, 1.0)]]

print(newPrediction)
