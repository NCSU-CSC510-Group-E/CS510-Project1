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

## Running the tests

You can run a simple end-to-end test of LDA simply by typing 
```
python analysis --verbose
```

For help with command-line options, run 
```
python analysis --help
```

## Deployment

There is the beginning of a useful Ansible script to deploy this code
in the ansible folder, but that script is currently not functional.
