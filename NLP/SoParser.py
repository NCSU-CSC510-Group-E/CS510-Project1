# Instructions: 
# Put 'posts-1.xml' in the same folder as this file

import xml.etree.ElementTree as et
import os
outputDir = ['./soFileOutput/body/','./soFileOutput/tags/']
if not os.path.exists(os.path.dirname(outputDir[0])):
    os.makedirs(os.path.dirname(outputDir[0]))
if not os.path.exists(os.path.dirname(outputDir[1])):
    os.makedirs(os.path.dirname(outputDir[1]))

# try:
#     os.makedirs(os.path.dirname('./body/'))
# except OSError as e:
#     if e.errno != errno.EEXIST:
#         raise
# try:   
#     os.makedirs(os.path.dirname('./tags/'))
# except OSError as e:
#     if e.errno != errno.EEXIST:
#         raise

document = et.iterparse("posts-1.xml", events=("start", "end"))
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
        f.write(Body.encode('utf8'))
        f.close()
        
        # generate and save post content to file file
        filename = outputDir[1] + str(Id) + '_' + 'tags.txt' 
        f = open(filename,'w')
        f.write(Tags.encode('utf8'))
        f.close()
        print i
    i += 1

    if i > 2000:
        break

elem.clear()


# try:
#     import cElementTree as ET
# except ImportError:
#   try:
#     # Python 2.5 need to import a different module
#     import xml.etree.cElementTree as ET
#   except ImportError:
#     exit_err("Failed to import cElementTree from any known place")      

# def find_in_tree(tree, node):
#     found = tree.find(node)
#     if found == None:
#         print "No %s in file" % node
#         found = []
#     return found  

# # Parse a xml file (specify the path)
# def_file = "posts.xml"
# try:
#     dom = ET.iterparse(open(def_file, "r"))
#     root = dom.getroot()
# except:
#     # exit_err("Unable to open and parse input definition file: " + def_file)
#     print 'not find'
# # Parse to find the child nodes list of node 'Id'
# fwdefs = find_in_tree(root,"Id")