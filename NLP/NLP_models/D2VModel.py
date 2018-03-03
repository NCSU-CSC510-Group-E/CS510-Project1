import gensim
from os import listdir
from random import randint
#from docToExcel import docToExcel
from shutil import copyfile
from multiprocessing import cpu_count
from smart_open import smart_open
from numpy import linalg

"""
Gensim Doc2Vec needs model training data in an iterator object
- modified to iterate through documents instead of a list
"""
class TaggedDocs():
    def __init__(self, data_dir, tokens_only=False):
        """
        docData = the raw contents string of the documents 
        """
        self.data_dir = data_dir
        self.filenames = [file for file in listdir(data_dir) if file.endswith('.txt')]
        self.tokens_only = tokens_only

    def __iter__(self):

        #read the corpus - the collection or set of documents
        #Documents are in body/ directory of stackoverflow input
        #gives it new integer tag/label to save space in case of large filenames

        for i, filename in enumerate(self.filenames):
            file = smart_open(self.data_dir + filename, 'rb')
            doc = file.read().decode("utf-8") #get past unicode
            file.close()

                       
            #gensim has built in tokenizer - remove punctuation, set to lowercase, split into list of words...
            if self.tokens_only:
                yield gensim.utils.simple_preprocess(doc)

            else:
                yield gensim.models.doc2vec.TaggedDocument(words=gensim.utils.simple_preprocess(doc),tags=[i])


    ## With the current gensim implementation, all label vectors are stored separately in RAM.
    ## they report being able to run 2 million different sentences no problem, however


class D2VModel():
    def __init__(self, model_name):
        self.model_name = model_name
        self.cores = cpu_count()
        assert gensim.models.doc2vec.FAST_VERSION > -1


        """
        Instructions:
        create the corpus
        build the model
        train model
        save model
        """

    def createCorpus(self, directory, tokens_only=False):
        #TaggedDocs acts as a iterator
        print()
        print("Creating Corpus...")
        if tokens_only: #testing, not training. Doesn't use tags.
            corpus = TaggedDocs(directory, True)
        else:
            corpus = TaggedDocs(directory) 

        self.corpus = corpus
        print("Corpus Created")
        print()

    def createModel(self, dm=1, vector_size=300, negative=5, window=5, min_count=2, epochs=20, dm_concat=1, dm_mean=0):
        print()
        print("Creating Model...")
        #create doc2vec model
        model = gensim.models.doc2vec.Doc2Vec(dm=dm, vector_size=vector_size, negative=negative, window=window, min_count=min_count, epochs=epochs, dm_concat=dm_concat, dm_mean=dm_mean, workers=self.cores)
        self.model = model
        print("Model " + str(model) + " Created")
        print()

    def trainModel(self):
        model = self.model
        print()
        print("Training Model ", str(model))

        #build vocabulary (dictionary accessible via mode.wv.vocab of all unique words extracted 
        #from the training corpus) with the frequency counts (model.wv.vocan['word'].count)
        model.build_vocab(self.corpus)

        #Train
        model.train(self.corpus, total_examples=model.corpus_count, epochs=model.epochs)

        self.model = model
        print("Model Trained")
        print()

    def saveModel(self):
        #save model to ./docModels folder
        print()
        print("Saving Model ", self.model_name)
        self.model.save("./docModels/" + self.model_name + ".model")
        print("Model Saved")
        print()

    def loadModel(self, filename):
        # LOAD
        print()
        print("Loading Model ", filename)
        model_loaded = gensim.models.Doc2Vec.load(filename)
        print("Model Loaded")
        print()

        self.model = model_loaded

    def infoRet(self, test_corpus1, test_corpus2):
        """
        Information Retrieval Test. Can the model accuratly predict 
        whether two documents are similar or not in comparison to another?
        @params - test_corpus2 is the corpus that needs twice as many documents
        """
        print()
        print("Starting Information Retrieval on", str(self.model))

        model = self.model
        used1 = []
        used2 = []
        correct = 0
        count = 0
        n1 = len(test_corpus1.filenames)
        n2 = len(test_corpus2.filenames)

        x = randint(0, n1-1) #randint is inclusive
        y1 = randint(0, n2-1)
        y2 = randint(0, n2-1)
        
        #cant use indexing on an iterator, have to add TaggedDocs to a list
        print("Creating first list")
        tc1 = [doc for doc in test_corpus1]
        print("Creating second list")
        tc2 = [doc for doc in test_corpus2]

        #find minimum number of times to run test
        min_ = min(n1, (n2)//2)

        #INFER A VECTOR without having to retrain via cosine similarity
        #use random documents from the corpuses
        print("Calculating inferred_vectors...")
        for i in range(min_):
            while x in used1:
                x = randint(0, n1-1)

            used1.append(x)

            while y1 in used2:
                y1 = randint(0, n2-1)

            used2.append(y1)

            while y2 in used2:
                y2 = randint(0, n2-1)

            used2.append(y2)

            x_vector = model.infer_vector(tc1[x]) #only tokens (no tags) don't have to call .words
            y1_vector = model.infer_vector(tc2[y1])
            y2_vector = model.infer_vector(tc2[y2])

            #y1 and y2 should be closer in distance to each other than x
            xy1 = linalg.norm(x_vector - y1_vector)
            xy2 = linalg.norm(x_vector - y2_vector)
            y1y2 = linalg.norm(y1_vector - y2_vector)

            if min(xy1, xy2, y1y2) == y1y2:
                correct += 1

            count += 1
            if (count % 500) == 0:
                print("Count:", count)

        return (correct, count)



        






def main():
    #Directories of posts
    train_python_javascript = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/trainPythonJavascript/'
    test_javascript = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/testJavascript/'
    test_python = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/testPython/'



    # ----  ----

    #initialzie objects
    dm_mean = D2VModel("")
    dm_concat = D2VModel("")
    dbow = D2VModel("")

    #create training corpus
    all_models = [dm_mean, dm_concat, dbow]

    #load models if an error during testing
    # dm_mean.loadModel('C:/Users/xocho/OneDrive/CS510-Project1/NLP/docModels/dmM_python_javascript.model')
    # dm_concat.loadModel('C:/Users/xocho/OneDrive/CS510-Project1/NLP/docModels/dmC_python_javascript.model')
    # dbow.loadModel('C:/Users/xocho/OneDrive/CS510-Project1/NLP/docModels/dbowM_python_javascript.model')

    #create training corpus
    for m in all_models:
        m.createCorpus(train_python_javascript)

    #create models
    dm_mean.createModel(dm=1, vector_size=300, negative=3, window=3, min_count=1, epochs=20, dm_concat=0, dm_mean=1)
    dm_concat.createModel(dm=1, vector_size=300, negative=3, window=3, min_count=1, epochs=20, dm_concat=1, dm_mean=0)
    dbow.createModel(dm=0, vector_size=300, negative=3, window=3, min_count=1, epochs=20, dm_concat=0, dm_mean=0)

    # #train models
    for mo in all_models:
        mo.trainModel()
        mo.saveModel()


    #create test corpuses
    testPython = TaggedDocs(test_python, True)
    testJavascript = TaggedDocs(test_javascript, True)


    # ----  ----



    #to compare:

    #INFER A VECTOR without having to retrain via cosine similarity
    #vector = model.infer_vector(['words', 'in', 'a', 'list'])

    #you can do this with already trained data:
    #vector = model.infer_vector(train_corpus[id].words) where id is the given tag

    #MOST SIMILAR - find the most similar vector in the trained corpus to the given one
    # similar = model.docvecs.most_similar([vector], topn=1)  change topn for number wanted to be returned
    #similar[index] will return data about the vector


    ## TEST RANDOM NEW DOC ##
    """
    doc_id = random.randint(0, len(test_corpus)-1)
    inferred_vector = model.infer_vector(test_corpus[doc_id])
    similar = model.docvecs.most_similar([inferred_vector], topn=1)
    similar[index]
    """

    ## TEST RANDOM TRAINED DOC ##
    """
    doc_id = random.randint(0, len(train_corpus)-1)
    inferred_vector = model.infer_vector(train_corpus[doc_id])
    similar = model.docvecs.most_similar([inferred_vector], topn=1)
    similar[index]
    """

   # make a graph? docToExcel(inferred_vectors, similar_vectors, title)

        

    

        



if __name__ == "__main__":
	main()