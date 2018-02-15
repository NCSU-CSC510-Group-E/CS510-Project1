import xml.etree.ElementTree as et

document = et.iterparse("posts.xml", events=("start", "end"))
i = 0
for event, elem in document:
    Id = elem.get('Id')
    Body = elem.get('Body')
    # print (type(Body))
    if Id and Body:
        filename = str(Id) + '_' + 'post.txt' 
        print(filename)
        # print (type(Body))
        # content = unicode(Body, 'encoding')
        f = open(filename,'w')
        f.write(Body.encode('utf8'))
        f.close()
        # print(content)
    i += 1

    if i > 100:
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