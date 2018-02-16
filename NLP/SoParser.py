# Instructions: 
# worked in python 2.7
from HTMLParser import HTMLParser
import xml.etree.ElementTree as et
import os

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def soParser(path_to_XML = "./posts-1.xml", path_to_output = './soFileOutput/', numFileNeed = 200):
    outputDir = [path_to_output + 'body/', path_to_output + 'tags/']
    if not os.path.exists(os.path.dirname(outputDir[0])):
        os.makedirs(os.path.dirname(outputDir[0]))
    if not os.path.exists(os.path.dirname(outputDir[1])):
        os.makedirs(os.path.dirname(outputDir[1]))

    document = et.iterparse(path_to_XML, events=("start", "end"))
    i = 0
    for event, elem in document:
        # print elem.keys()   # read the keys of each element
        Id = elem.get('Id')
        Body = elem.get('Body')
        Tags = elem.get('Tags')
        if Id and Body and Tags:
            # generate and save post content to file file
            filename = outputDir[0] + str(Id) + '_' + 'body.txt' 
            f = open(filename,'w')
            f.write(strip_tags(Body).encode('utf8'))
            f.close()
            
            # generate and save post content to file file
            filename = outputDir[1] + str(Id) + '_' + 'tags.txt' 
            f = open(filename,'w')
            f.write(Tags.encode('utf8'))
            f.close()
            
        i += 1
        if i > numFileNeed:
            print i
            break

    elem.clear()
soParser()
