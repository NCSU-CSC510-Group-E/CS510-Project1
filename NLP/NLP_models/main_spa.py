from D2VModel import D2VModel, TaggedDocs
from random import randint

def main():
    #Directories of posts
    train_python_javascript = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/trainPythonJavascript/'
    train_python = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/pythonPosts/'
    train_javascript = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/javascriptPosts/'


    # ---- Sentiment Prediction Accuracy ----

    #initialzie objects
    dm_mean = D2VModel("dmM_Py")
    dm_concat = D2VModel("dmC_Py")
    dbow = D2VModel("dbow_Py")

    #create training corpus
    #all_models = [dm_mean, dm_concat, dbow]
    all_models = [dbow]

    #load models if an error during testing
    # dm_mean.loadModel(' ')
    # dm_concat.loadModel(' ')
    # dbow.loadModel(' ')

    #create training corpus
    for m in all_models:
        m.createCorpus(train_python)

    #create models
    dm_mean.createModel(dm=1, vector_size=100, negative=5, window=5, min_count=1, epochs=20, dm_concat=0, dm_mean=1)
    dm_concat.createModel(dm=1, vector_size=100, negative=5, window=5, min_count=1, epochs=20, dm_concat=1, dm_mean=0)
    dbow.createModel(dm=0, vector_size=100, negative=10, window=0, min_count=1, epochs=20, dm_concat=0, dm_mean=0)

    # #train models
    for mo in all_models:
        mo.trainModel()
        mo.saveModel()


    #send to sentiment prediction accuracy analysis
    for mod in all_models:
        results = mod.spa()
        print()
        print(mod.model)
        print("Correct: ", results[0])
        print("Out of: ", results[1])
        print("Min: " + str(results[2]) + " Max: " + str(results[3]))
        print("Mean: " + str(results[4]) + " Median: " + str(results[5]))
        print()



    # ---- End of Info Retieval ----



if __name__ == "__main__":
    main()