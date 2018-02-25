"""
Instructions: 
worked in python 2.7
Function: take stackoverflow post.xml file, parses to two text file for each \
post, one file contains the post body, another contains the tags for that post. 
"""
from HTMLParser import HTMLParser
import xml.etree.ElementTree as et
import os

"""
Functions and classes to strip html tags from text
"""
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

"""
Function to strip html tags from text
"""
def strip_html_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

"""
Function to strip angle brackets from text
"""
def strip_bracket(str):
    s = str.replace('><',',')
    s = s.replace('<','')
    return s.replace('>','')

"""
main function to do the parser work
"""
def so_parser(path_to_XML="./posts-1.xml", path_to_output='./soFileOutput/', num_file_need=200):
    output_dir = [path_to_output + 'body/', path_to_output + 'tags/']
    
    #check if the output directory exists, if not, creat it
    if not os.path.exists(os.path.dirname(output_dir[0])):
        os.makedirs(os.path.dirname(output_dir[0]))
    if not os.path.exists(os.path.dirname(output_dir[1])):
        os.makedirs(os.path.dirname(output_dir[1]))

    document = et.iterparse(path_to_XML, events=("start", "end"))
    i = 0
    for event, elem in document:
        post_id = elem.get('Id')
        post_body = elem.get('Body')
        post_tags = elem.get('Tags')
        if post_id and post_body and post_tags:
            # generate and save post content to file file
            filename = output_dir[0] + str(post_id) + '.txt'
            f = open(filename, 'w')
            f.write(strip_html_tags(post_body).encode('utf8'))
            f.close()

            # generate and save post content to file file
            filename = output_dir[1] + str(post_id) + '.txt'
            f = open(filename, 'w')
            tags = post_tags.encode('utf8')
            f.write(strip_bracket(tags))
            f.close()

        # to get only a few of file, not to parse the whole document
        i += 1
        if i > num_file_need:
            print i
            break

    elem.clear()

# run the parser function.
if __name__ == '__main__':
    so_parser()
