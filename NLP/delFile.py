import os
from os import listdir

"""
Delete dangerous files out of tags folder that were captured by Microsoft's Defender from the body
"""


def deleteFile(directory, filenames):
        trojans = ['55064.txt', '319265.txt', '383413.txt', '426517.txt', '456861.txt', '558421.txt', '697121.txt', '756020.txt', '776046.txt', '889594.txt', '1281677.txt']

        for filename in filenames:
            if filename in trojans:
                print(filename)
        
                os.remove(directory + filename)
                

def main():
    directory = 'D:/allPosts3/'
    
    body = directory + 'body/'
    tags = directory + 'tags/'

    bodyFiles = [file for file in listdir(body) if file.endswith('.txt')]
    tagFiles = [file for file in listdir(tags) if file.endswith('.txt')]

    print("BODY")
    deleteFile(body, bodyFiles)
    print()

    print("TAGS")
    deleteFile(tags, tagFiles)

    

if __name__ == "__main__":
    main()