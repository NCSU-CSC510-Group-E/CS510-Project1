import gensim
from os import listdir
from random import randint
#from docToExcel import docToExcel
from shutil import copyfile
from multiprocessing import cpu_count
from smart_open import smart_open

"""
Gensim Doc2Vec needs model training data in an iterator object
- modified to iterate through documents instead of a list
"""
class TaggedDocs(object):
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

    def createModel(self, dm=1, vector_size=300, window=10, min_count=2, epochs=20, dm_concat=1, dm_mean=0):
        print()
        print("Creating Model...")
        #create doc2vec model
        model = gensim.models.doc2vec.Doc2Vec(dm=dm, vector_size=vector_size, window=window, min_count=min_count, epochs=epochs, dm_concat=dm_concat, dm_mean=dm_mean, workers=self.cores)
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
        print("Loading Model ", filename)
        self.model_name = filename
        model_loaded = doc2vec.Doc2Vec.load(filename)
        print("Model Loaded")

        self.model = model_loaded

    def infoRet(self, test_corpus1, test_corpus2):
        """
        Information Retrieval Test. Can the model accuratly predict 
        whether two documents are similar or not in comparison to another?
        @params - test_corpus2 is the corpus that needs twice as many documents
        """
        model = self.model
        used1 = []
        used2 = []
        correct = 0
        count = 0
        x = randint(0, test_corpus1.corpus_count)
        y1 = randint(0, test_corpus1.corpus_count)
        y2 = randint(0, test_corpus1.corpus_count)
        
        

        #find minimum number of times to run test
        min_ = min(test_corpus1.corpus_count, (test_corpus2.corpus_count)//2)

        #INFER A VECTOR without having to retrain via cosine similarity
        #use random documents from the corpuses
        for i in range(min_):
            while x in used1:
                x = randint(0, test_corpus1.corpus_count)

            used1.append(x)

            while y1 in used2:
                y1 = randint(0, test_corpus1.corpus_count)

            used2.append(y1)

            while y2 in used2:
                y2 = randint(0, test_corpus1.corpus_count)

            used2.append(y2)

            x_vector = model.infer_vector(test_corpus1[x].words)
            y1_vector = model.infer_vector(test_corpus1[y1].words)
            y2_vector = model.infer_vector(test_corpus1[y2].words)

            #y1 and y2 should be closer in distance to each other than x
            xy1 = abs(x_vector - y1_vector)
            xy2 = abs(x_vector - y2_vector)
            y1y2 = abs(y1_vector - y2_vector)

            if min(xy1, xy2, y1y2) is y1y2:
                correct =+ 1

            count += 1

        return (correct, count)

        


def createRandomMix(numToTrain, numToTest, inputDirectory, trainDirectory, testDirectory):
    """
    copy and paste random files from one folder into another
    for testing so that the test files are not trained on
    """
    filenames = listdir(inputDirectory) #returns a list of filenames in order
    used = []
    ap = used.append

    print("copy-pasting files...")

    #add files to training folder
    for i in range(numToTrain):
        x = random.randint(0, len(filenames)-1)
        while x in used:
            x = random.randint(0, len(filenames)-1)
        ap(x)
        source = inputDirectory + filenames[x]
        destination = trainDirectory + filenames[x]
        copyfile(source, destination)

    #add files to testing folder that were not trained on
    for k in range(numToTest):
        y = random.randint(0, len(filenames)-1)
        while y in used:
            y = random.randint(0, len(filenames)-1)
        ap(y)
        source = inputDirectory + filenames[y]
        destination = testDirectory + filenames[y]
        copyfile(source, destination)

    print("done copy-pasting files")



def main():
    #Directories of posts
    train_python_javascript = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/trainPythonJavascript/'
    test_javascript = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/testJavascript/'
    test_python = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/testPython/'


    # ---- Create Training and Testing Folders for Info Retrieval ----
    # createRandomMix(25000, 30000, 'D:/javascriptPosts/', train_dir, test_dir1)
    # createRandomMix(25000, 15000, 'D:/pythonPosts/', train_dir, test_dir2)



    # ---- Info Retrieval ----

    #initialzie objects
    dm_mean = D2VModel("dmM_python_javascript")
    dm_concat = D2VModel("dmC_python_javascript")
    dbow = D2VModel("dbowM_python_javascript")

    #create training corpus
    all_models = [dm_mean, dm_concat, dbow]

    for m in all_models:
        m.createCorpus(train_python_javascript)

    #create models
    dm_mean.createModel(dm=1, vector_size=300, window=10, min_count=2, epochs=20, dm_concat=0, dm_mean=1)
    dm_concat.createModel(dm=1, vector_size=300, window=10, min_count=2, epochs=20, dm_concat=1, dm_mean=0)
    dbow.createModel(dm=0, vector_size=300, window=10, min_count=2, epochs=20, dm_concat=0, dm_mean=0)

    #train models
    for mo in all_models:
        mo.trainModel()
        mo.saveModel()

    #create test corpuses
    testPython = TaggedDocs(test_python, True)
    testJavascript = TaggedDocs(test_javascript, True)

    #send to information retrieval task
    for mod in all_models:
        results = mod.infoRet(testPython, testJavascript)
        print()
        print(mod.model)
        print("Correct: ", results[0])
        print("Out of: ", results[1])
        print()


    # ---- End of Info Retieval ----



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