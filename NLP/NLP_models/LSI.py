


from gensim.test.utils import common_dictionary, common_corpus
from gensim.models import LsiModel
from gensim import corpora, models

#Biuld corpus and dictionay
path_to_input = '/Users/zhangqi/CS510-Project1/NLP/soFileTrain/'
corpus = corpora.TextDirectoryCorpus(path_to_input, lines_are_documents=False)
Dictionary = corpus.dictionary
Dictionary.id2token = dict([[v,k] for k,v in Dictionary.token2id.items()])

#training our lsi model based on corpus            
model = LsiModel(corpus, id2word=Dictionary.id2token)
vectorized_corpus = model[common_corpus]  # vectorize input copus in BoW format


    
#  >>> from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
# >>> from gensim.models import LsiModel
# >>>
# >>> model = LsiModel(common_corpus[:3], id2word=common_dictionary)  # train model
# >>> vector = model[common_corpus[4]]  # apply model to BoW document
# >>> model.add_documents(common_corpus[4:])  # update model with new documents
# >>> tmp_fname = get_tmpfile("lsi.model")
# >>> model.save(tmp_fname)  # save model
# >>> loaded_model = LsiModel.load(tmp_fname)  # load model   
    

    
    
        
        
