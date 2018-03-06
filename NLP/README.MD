# CSC510 Group P Project

Our project is intended to apply NLP algorithms to books.  The current
prototype trains on Stack Overflow data which we parse from an XML
dump and suggests the tags on the post as a proof of concept.

## Getting Started

To run the program, you will need Python 3.5+.  Run the program with
'python analysis.py' and pass any command line parameters to that as appropraite
### Prerequisites

To run this code, you will need the following python libraries:
* [Click ](http://click.pocoo.org/5/)
* [Gensim](https://radimrehurek.com/gensim/)
* [Peewee](http://docs.peewee-orm.com/en/latest/)

### Installing

The required dependencies should be installable via Pip in most
cases.  
```
pip install click
pip install gensim
pip install peewee
```

## Running the test

You can run a simple end-to-end test of LDA simply by typing 
```
python analysis --verbose
```

For help with command-line options, run 
```
python analysis --help
```

## Code Breakdown
*
  [Analysis.py](https://github.com/NCSU-CSC510-Group-E/CS510-Project1/blob/master/NLP/analysis.py)
  
  This file houses the CLI environment.  All code relating to the
  command-line options and their defaults resides in this file.
*
  [prototype.py](https://github.com/NCSU-CSC510-Group-E/CS510-Project1/blob/master/NLP/prototype.py)
  
  This file houses the "main" method of the CLI.  It is where the
  lion's share of the prediction and validation code exist for this prototype
*
  [NLP_Models/LDA.py](https://github.com/NCSU-CSC510-Group-E/CS510-Project1/blob/master/NLP/NLP_models/LDA.py)
  
  This file houses a helper class built around Gensim's LDA class.
  It contains methods to conveinently train and cache an LDA model
  to an interface against which other NLP algorithms could be
  implemented generically.  
*
  [NLP_Models/Doc2Vec.py](https://github.com/NCSU-CSC510-Group-E/CS510-Project1/blob/master/NLP/NLP_models/D2VModel.py)
  
  This file is similar to the above LDA file, but for Doc2Vec instead.
* [SoParser*](https://github.com/NCSU-CSC510-Group-E/CS510-Project1/blob/master/NLP/SoParser.py) 
  The SoParser files contain the tools we used to process the Stack
  Overflow data to a useful data set (a test ofwhich can already be
  found in the soFileTest and soFileTrain directories, so you will not
  need to run this step manually in most cases.)
  
  
  

## Deployment

There is the beginning of a useful Ansible script to deploy this code
in the ansible folder, but that script is currently not functional.
