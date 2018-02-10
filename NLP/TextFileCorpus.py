"""
This class is intended to be a custom iterator over the set of docuemnts being parsed.
In our case, we will use this method to parse all text files in a given directory, 
loading them into memory one at a time.  
"""

import os # Used to read all files ina  directory
import gensim

class TextFileCorpus(gensim.corpora.TextCorpus):

   def __init__(self, input=None, dictionary=None, metadata=False, character_filters=None,
                tokenizer=None, token_filters=None):

       self.pathToFiles = input

       gensim.corpora.TextCorpus.__init__(input, dictionary, metadata, character_filters, tokenizer, token_filters)

       self._debugging = False;

    def get_texts(self):
        """
        This is the function that actually reads the files from the disk
        """
