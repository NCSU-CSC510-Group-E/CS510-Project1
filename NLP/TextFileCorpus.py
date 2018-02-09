"""
This class is intended to be a custom iterator over the set of docuemnts being parsed.
In our case, we will use this method to parse all text files in a given directory, 
loading them into memory one at a time.  
"""

import os # Used to read all files ina  directory

class TextFileCorpus(object):

   def __init__(object, path_to_files, debugging=False):
       self._debugging = debugging;
       self._path = path_to_files
       
   def __iter__(self):
       if(self._debugging): print('Beginning iteration over corpus')

       listOfInputFiles = os.listdir(self._path);

       for fileName in listOfInputFiles: 
            for line in open(fileName):

                if(self.debugging): print('Retrieving a line from our file')

                # assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(line.lower().split()) 
