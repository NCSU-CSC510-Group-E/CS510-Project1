from D2VModel import D2VModel, TaggedDocs
from random import randint

def main():
    #Directories of posts
    train_python_javascript = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/trainPythonJavascript/'
    train_python = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/pythonPosts/'
    train_javascript = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/javascriptPosts/'
    train_all = 'C:/Users/xocho/OneDrive/CS510-Project1/NLP/allPosts/body/'
    test_list = [[train_python_javascript, "PJ"], [train_python, "py"], [train_javascript, "js"]]

    # ---- Sentiment Prediction Accuracy ----
    for test in test_list:
        #initialzie objects
        dm_mean = D2VModel("dmM_" + test[1])
        dm_concat = D2VModel("dmC_" + test[1])
        dbow = D2VModel("dbow_" + test[1])

        #create training corpus
        all_models = [dm_mean, dm_concat, dbow]

        #load models if an error during testing
        # # dm_mean.loadModel(' ')
        # # dm_concat.loadModel(' ')
        # dbow.loadModel('C:/Users/xocho/OneDrive/CS510-Project1/NLP/docModels/dbow_Py.model')
        # all_models = [dbow]

        #create training corpus
        for m in all_models:
            m.createCorpus(test[0])

        # #create models
        dm_mean.createModel(dm=1, vector_size=300, negative=5, window=5, min_count=1, epochs=20, dm_concat=0, dm_mean=1)
        dm_concat.createModel(dm=1, vector_size=300, negative=5, window=5, min_count=1, epochs=20, dm_concat=1, dm_mean=0)
        dbow.createModel(dm=0, vector_size=300, negative=10, window=0, min_count=1, epochs=20, dm_concat=0, dm_mean=0)

        #train models
        for mo in all_models:
            mo.trainModel()
            mo.saveModel()


    #send to sentiment prediction accuracy analysis
    # for mod in all_models:
    #     results = mod.vpa()
    #     print()
    #     print(mod.model)
    #     print("Correct: ", results[0])
    #     print("Out of: ", results[1])
    #     print("Min: " + str(results[2]) + " Max: " + str(results[3]))
    #     print("Mean: " + str(results[4]) + " Median: " + str(results[5]))
    #     print()



    # ---- End of Info Retieval ----



if __name__ == "__main__":
    main()