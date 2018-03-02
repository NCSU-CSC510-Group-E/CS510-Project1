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
def so_parser(num_train_need=1000,num_test_need=10, path_to_XML="./posts-1.xml", path_to_output_train='./soFileTrain/', path_to_output_test='./soFileTest/'):
    output_dir = [path_to_output_train + 'body/', path_to_output_train + 'tags/', path_to_output_test + 'body/', path_to_output_test + 'tags/']
    
    #check if the output directory exists, if not, creat it
    for directory in output_dir:
        if not os.path.exists(os.path.dirname(directory)):
            os.makedirs(os.path.dirname(directory))

    document = et.iterparse(path_to_XML, events=("start", "end"))
    i = 0
    for event, elem in document:
        post_id = elem.get('Id')
        post_body = elem.get('Body')
        post_tags = elem.get('Tags')
        
        pre_define_tags = ['javascript', 'python', 'database', 'sql', 'java']
        
        if post_id and post_body and post_tags:
            
            tags = strip_bracket(post_tags.encode('utf8')).split(',')
            
            for pre_tag in pre_define_tags:
                if pre_tag in tags:
                # if True:
                    # generate and save post content to file file
                    if i > num_train_need:
                        body_filename = output_dir[2] + str(post_id) + '.txt'
                        tag_filename = output_dir[3] + str(post_id) + '.txt'
                    else:
                        body_filename = output_dir[0] + str(post_id) + '.txt'
                        tag_filename = output_dir[1] + str(post_id) + '.txt'
                    f = open(body_filename, 'w')
                    f.write(strip_html_tags(post_body).encode('utf-8'))
                    f.close()

                    # generate and save post content to file file
                    f = open(tag_filename, 'w')
                    tags = post_tags.encode('utf-8')
                    f.write(strip_bracket(tags))
                    f.close()
                    i += 1
                    break

        # to get only a few of file, not to parse the whole document

        if i > num_train_need + num_test_need:
            print i
            break

    elem.clear()

# run the parser function.
if __name__ == '__main__':
    so_parser()
