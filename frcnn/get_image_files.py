from client import *
import os,sys,thread
import time

def run_get_images(token,image_directory):
    in_image_directory = "./images"

    print("getImage_no")
    [no_of_images, status] = get_no_of_images(token)
    if status==0:
        print "Token, Incorrect or Expired. Bye!"
        sys.exit()

    print("getImages")
    for w in range (1,int(no_of_images)+1,1):
        if(len(os.listdir(in_image_directory))) > 20:
            print("sleeping -- image overflow")
            time.sleep(5)
        elif get_image(token,w)==0:             # If get_image failed, exit.
            print "Get Image Failed, Exiting, Bye!"
            sys.exit()
        else:
            print "Image Stored in client directory "+in_image_directory+"/"+str(w)+".jpg"


