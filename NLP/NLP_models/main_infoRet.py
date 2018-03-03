from D2VModel import D2VModel, TaggedDocs

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
    dm_mean = D2VModel("dmM_python_javascript2")
    dm_concat = D2VModel("dmC_python_javascript2")
    dbow = D2VModel("dbowM_python_javascript2")

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

    #send to information retrieval task
    for mod in all_models:
        results = mod.infoRet(testPython, testJavascript)
        print()
        print(mod.model)
        print("Correct: ", results[0])
        print("Out of: ", results[1])
        print()


    # ---- End of Info Retieval ----



if __name__ == "__main__":
    main()