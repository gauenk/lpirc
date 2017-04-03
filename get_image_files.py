import os,sys
import pycurl
import subprocess
import time
from urllib import urlencode
from StringIO import StringIO
import atexit,cv2
from PIL import Image
import numpy as np
host_ipaddress = '192.168.1.2'
host_port = '5033'
username = 'lpirc'
password = 'pass'
image_directory = './images'
temp_directory = './temp'

def run_get_images(token,image_directory,net):
    in_image_directory = "./images"
    time_to_live = 10000

    ## START THE GET_DETS PROCESS
    p = subprocess.Popen(['python', 'get_detections.py'], stdin = subprocess.PIPE)
    atexit.register(p.kill)
    print(type(net))
    p.stdin.write(repr(net)+"\n")
    a = repr([[token,"192.168.1.2","5033"]]+[time_to_live])+"\n"
    p.stdin.write(a)

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
        elif p_get_image(token,w,p)==0:             # If get_image failed, exit.
            print "Get Image Failed, Exiting, Bye!"
            sys.exit()
        else:
            
            print "Image sent to get_dets"
            #print "Image Stored in client directory "+in_image_directory+"/"+str(w)+".jpg"


def get_image(token, image_number):
    global image_directory
    global temp_directory
    c = pycurl.Curl()
    c.setopt(c.URL, host_ipaddress+':'+host_port+'/image')#/?image='+str(image_number))
    post_data = {'token':token, 'image_name':str(image_number)}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS,postfields)
    try:
            os.stat(temp_directory)
    except:
            os.mkdir(temp_directory)
    try:
            os.stat(image_directory)
    except:
            os.mkdir(image_directory)
    # Image will be saved as a file
    with open(temp_directory+'/'+str(image_number)+'.jpg', 'wb') as f:
        c.setopt(c.WRITEDATA, f)
        c.perform()
        status = c.getinfo(pycurl.HTTP_CODE)
        c.close()
    if status == 200:
        # Server replied OK so, copy the image from temp_directory to image_directory
        shutil.move(temp_directory+'/'+str(image_number)+'.jpg',image_directory+'/'+str(image_number)+'.jpg')
        return 1
    elif status == 401:
        # Server replied 401, Unauthorized Access, remove the temporary file
        os.remove(temp_directory+'/'+str(image_number)+'.jpg')
        print "Invalid Token\n"
        return 0
    else:
        # Server replied 406, Not Acceptable, remove the temporary file
        os.remove(temp_directory+'/'+str(image_number)+'.jpg')
        print "The image number is not Acceptable\n" 
        return 0

def p_get_image(token, image_number,p):

    c = pycurl.Curl()
    c.setopt(c.URL, host_ipaddress+':'+host_port+'/image')#/?image='+str(image_number))
    post_data = {'token':token, 'image_name':str(image_number)}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS,postfields)
    # Image will be saved as a file
    with open(temp_directory+'/'+str(image_number)+'.jpg', 'wb') as f:
        buffer = StringIO()
        c.setopt(c.WRITEDATA,buffer)
        #print(mbuffer)
        c.perform()
        status = c.getinfo(pycurl.HTTP_CODE)
        c.close()
    if status == 200:
        # Server replied OK so, copy the image from temp_directory to image_directory
        print(type(buffer))
        print(buffer)
        print(type(buffer.getvalue()),"val")
        #p.stdin.write(buffer)
        p.stdin.write(buffer.getvalue())
        #img = np.asarray(Image.open(buffer), dtype=np.uint8)
        # x = np.array_repr(img).replace("\n","").strip() ## parse detections for safe piping
        # print(type(img))
        # print(repr(img))
        # print(x)
        # print("\n\n^X\n\n")
        # p.stdin.write(x+"\n")
        #shutil.move(temp_directory+'/'+str(image_number)+'.jpg',image_directory+'/'+str(image_number)+'.jpg')
        return 1
    elif status == 401:
        # Server replied 401, Unauthorized Access, remove the temporary file
        os.remove(temp_directory+'/'+str(image_number)+'.jpg')
        print "Invalid Token\n"
        return 0
    else:
        # Server replied 406, Not Acceptable, remove the temporary file
        os.remove(temp_directory+'/'+str(image_number)+'.jpg')
        print "The image number is not Acceptable\n" 
        return 0

def get_no_of_images(token):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, host_ipaddress+':'+host_port+'/no_of_images')
    post_data = {'token':token}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS,postfields)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    status = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    if status == 200:
        return [buffer.getvalue(), 1]
    else:
        return [buffer.getvalue(), 0]

if __name__ == "__main__":
    pass
    #run_get_images(token,image_directory,net)
