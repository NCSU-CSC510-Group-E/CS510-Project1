"""
Python 3. Might work with 2.7
Find posts with a certain tag and copy-paste posts into a new folder
"""
import os
import shutil


def tagParser(tag='python', input_path='./allPosts3/'):
    output_path = './' + tag + 'Posts/'
    #check if the output directory exists, if not, create it
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    directory = os.listdir(input_path + "tags/") #returns a list of filenames in order
    
    i = 0
    for filename in directory:
        post = open(input_path + "tags/" + filename, 'r')
        tags = post.readline().split(',')  #generate list of string tags; tags file should only have one line
    
        #check if post contains the specified tag
        if (tag in tags) and ('database' not in tags) and ('java' not in tags) and ('c#' not in tags) and ('.net' not in tags) and ('javascript' not in tags):

            #copy and paste post body into new folder
            src = input_path + 'body/' + filename
            dst = output_path + filename
            shutil.copyfile(src, dst)

            i += 1
            if (i % 10000) == 0:
                print("File Count: ", i)


        post.close()


    print("File Count: ", i) #Final count



# run the parser function.
if __name__ == '__main__':
    tagParser()