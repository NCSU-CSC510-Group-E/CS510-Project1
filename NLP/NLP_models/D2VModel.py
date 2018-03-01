import gensim
from os import listdir
import random
#from docToExcel import docToExcel
import shutil

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
        
    def __iter__(self):

        #read the corpus - the collection or set of documents
        #Documents are in body/ directory of stackoverflow input
        #gives it new integer tag/label to save space in case of large filenames

        for i, filename in enumerate(self.filenames):
            file = open(self.data_dir + filename, 'r')
            doc = file.read()  #get string of entire document
            file.close()
                       
            #gensim has built in tokenizer - remove punctuation, set to lowercase, split into list of words...
            if tokens_only:
                yield gensim.utils.simple_preprocess(doc)

            else:
                yield gensim.models.doc2vec.TaggedDocument(words=gensim.utils.simple_preprocess(doc),tags=[i])


    ## With the current gensim implementation, all label vectors are stored separately in RAM.
    ## they report being able to run 2 million different sentences no problem, however
class D2VModel():
    def __init__(self, model_name, train_dir, test_dir1, test_dir2):
        self.model_name = model_name
        self.train_dir = train_dir
        self.test_dir1 = test_dir1
        self.test_dir2 = test_dir2

     def trainModel(self):
        """
        create the corpus
        build the model
        train model
        save model
        """

        #First, get corpus iterator
        train_corpus = TaggedDocs(self.train_dir) #both
        test_corpus1 = TaggedDocs(self.test_dir1, True) #javascript
        test_corpus2 = TaggedDocs(self.test_dir2, True)  #python

        #create do2vec model. dm=1 is for DM model
        model = gensim.models.doc2vec.Doc2Vec(dm=1, vector_size=300, window=10, min_count=2, epochs=20)

        #build vocabulary (dictionary accessible via mode.wv.vocab of all unique words extracted 
        #from the training corpus) with the frequency counts (model.wv.vocan['word'].count)
        model.build_vocab(train_corpus)

        #Train
        model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
        self.model = model

    def saveModel(self):
        #save model 
        print()
        print("Saving Model..")
        self.model.save(self.model_name)
        print("Model Saved")
        print()

    def loadModel(self, filename):
        # LOAD
        model_loaded = doc2vec.Doc2Vec.load(filename)
        self.model = model_loaded

    def infoRet():
        """
        Information Retrieval Test. Can the model accuratly predict 
        whether two documents are similar or not in comparison to another?
        """
        


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
            shutil.copyfile(source, destination)

        #add files to testing folder that were not trained on
        for k in range(numToTest):
            y = random.randint(0, len(filenames)-1)
            while y in used:
                y = random.randint(0, len(filenames)-1)
            ap(y)
            source = inputDirectory + filenames[y]
            destination = testDirectory + filenames[y]
            shutil.copyfile(source, destination)

        print("done copy-pasting files")

def main():

    model_name = 'javascript-python-model'
    train_dir = 'D:/trainPythonJavascript/'
    test_dir1 = 'D:/testJavascript/'
    test_dir2 = 'D:/testPython/'

    model = D2VModel(model_name, train_dir, test_dir1, test_dir2)

    # ---- Create Training and Testing Folders for Info Retrieval ----
    # createRandomMix(25000, 30000, 'D:/javascriptPosts/', train_dir, test_dir1)
    # createRandomMix(25000, 15000, 'D:/pythonPosts/', train_dir, test_dir2)



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