from D2VModel import D2VModel, TaggedDocs
import os
from random import randint
from shutil import copyfile

def createRandomMix(numToTrain, numToTest, inputDirectory, trainDirectory, testDirectory):
    """
    copy and paste random files from one folder into another
    for testing so that the test files are not trained on
    """

    #check if directories exists, if not, create them
    if not os.path.exists(os.path.dirname(trainDirectory)):
        os.makedirs(os.path.dirname(trainDirectory))
    if not os.path.exists(os.path.dirname(testDirectory)):
        os.makedirs(os.path.dirname(testDirectory))

    filenames = [file for file in os.listdir(inputDirectory)] #returns a list of filenames in order
    used = []
    ap = used.append

    print()
    print("copy-pasting files...")

    #add files to training folder
    for i in range(numToTrain):
        x = randint(0, len(filenames)-1) #randint is inclusive
        while x in used:
            x = randint(0, len(filenames)-1)
        ap(x)
        source = inputDirectory + filenames[x]
        destination = trainDirectory + filenames[x]
        copyfile(source, destination)

    #add files to testing folder that were not trained on
    for k in range(numToTest):
        y = randint(0, len(filenames)-1)
        while y in used:
            y = randint(0, len(filenames)-1)
        ap(y)
        source = inputDirectory + filenames[y]
        destination = testDirectory + filenames[y]
        copyfile(source, destination)

    print("done copy-pasting files")


def main():
    #Directories of posts
    
    #need / at end
    train_dir = '/'
    test_dir1 = '/'
    test_dir2 = '/'

    # ---- Create Training and Testing Folders for Info Retrieval ----
    # createRandomMix(int_to_train, int_to_test, dir_to_find_topic1, train_dir, test_dir1)
    # createRandomMix(int_to_train, int_to_test, dir_to_find_topic1, train_dir, test_dir2)
    ##### make sure test_dir2 is the directory that will test with twice as many documents #####


    # ---- Info Retrieval ----
    
    #initialzie objects
    dm_mean = D2VModel("dmM_" + name)
    dm_concat = D2VModel("dmC_" + name)
    dbow = D2VModel("dbowM_" + name)

    #create training corpus
    all_models = [dbow, dm_mean, dm_concat]

    #load models if an error during testing --> comment out training corpus, create models, and train models
    # dm_mean.loadModel('C:/Users/xocho/OneDrive/CS510-Project1/NLP/docModels/dmM_' + name + ".model")
    # dm_concat.loadModel('C:/Users/xocho/OneDrive/CS510-Project1/NLP/docModels/dmC_' + name + ".model")
    # dbow.loadModel('C:/Users/xocho/OneDrive/CS510-Project1/NLP/docModels/dbowM_' + name + ".model")

    #create training corpus
    for m in all_models:
        m.createCorpus(train_dir)

    #create models
    dbow.createModel(dm=0, vector_size=300, negative=10, window=0, min_count=1, epochs=50, dm_concat=0, dm_mean=0)
    dm_mean.createModel(dm=1, vector_size=300, negative=5, window=5, min_count=1, epochs=50, dm_concat=0, dm_mean=1)
    dm_concat.createModel(dm=1, vector_size=300, negative=5, window=5, min_count=1, epochs=50, dm_concat=1, dm_mean=0)
        
    #train models
    for mo in all_models:
        mo.trainModel()
        mo.saveModel()


    #create test corpuses
    testCorpus1 = TaggedDocs(test_dir1, True)
    testCorpus2 = TaggedDocs(test_dir2, True)

    #send to information retrieval task
    for mod in all_models:
        results = mod.infoRet(testCorpus1, testCorpus2)
        print()
        print(mod.model)
        print("Correct (Eucildean Distance): ", results[0])
        print("Correct (Cosine Disstance): ", results[1])
        print("Out of: ", results[2])
        print()


    # ---- End of Info Retieval ----



if __name__ == "__main__":
    main()