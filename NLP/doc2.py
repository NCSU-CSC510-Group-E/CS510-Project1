

##get txt documents from folder 'input'
from os import listdir
from os.path import isfile, join


def main()
    
    path_to_input = "./input"
    # the file names of the txt documents kept in a list
    docLabels = []
    docLabels = [file for file in listdir(path_to_input) if file.endswith('.txt')]


    # load text out of .txt documents to list - may have to change if content is too large
    data = []
    for doc in docLabels:
    data.append(open(path_to_input + doc, 'r')

if __name__ == "__main__":
    main()