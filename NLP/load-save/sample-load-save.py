## SAMPLE OF LOADING / SAVING LARGE DOCUMENT SIZES

from MyCorpus import MyCorpus
from gensim import corpora

INPUT_FILE = 'mycorpus.txt'
DICT_SAVE = 'dictionary' #class adds .dict 
DICT_LOAD = 'dictionary' #class adds .dict



def main():
    corpus = MyCorpus(INPUT_FILE)

    ## checking output of vectors to sample in tutorial
    for vector in corpus:
        print(vector)

    ## save dictionary object via genism
    corpus.saveDict(DICT_SAVE)

    ## load dictionary object via genism
    new_corpus = MyCorpus(INPUT_FILE, True)
    print()
    for vector2 in new_corpus:
        print(vector2)
    
    #print keys, values (words, frequency count)
    print(corpus._dict.token2id)
    print(new_corpus._dict.token2id)





if __name__ =="__main__":
    main()

