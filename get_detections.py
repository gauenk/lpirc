import os,sys,time
import _init_paths
import caffe
import subprocess
import atexit
from caffe import _caffe
from numpy import array, all, float32, uint8
import numpy as np
from PIL import Image
from StringIO import StringIO

caffe.set_mode_gpu()
caffe.set_device(0)
#img_dir = "./images/"
#mlist = os.listdir(img_dir)
n_classes= 21
pr_list = []
time_to_live = 1000
n_time = time.time()
post_data = None
net = None
ttl = None

print("IN DET")

while(time_to_live > 0):
    try:
        _img = raw_input()
        if net is None:
            data = _img
            net = data[0]
            continue
            
        if post_data is None:
            print("POST_DATA NONE\n\n\n")
            data = eval(_img)
            print(data)
            print("evaled the image\n\n\n")
            post_data = data[0]
            print(post_data)
            p = subprocess.Popen(['python', 'test.py'], stdin = subprocess.PIPE)
            p.stdin.write(repr(post_data)+"\n")
            ttl = data[1]
            print("SAFELY PARSED FROM PIPE\n\n\n")
            continue

        


        print(type(_img))
        print("GOT IMAGE\n\n")
        #print(bytearray(_img))
        buffer = StringIO(_img)
        print("MADE BUFFER")
        print(buffer)
        print(buffer.getvalue() == _img)
        #print(_img)
        #img = np.fromstring(_img, dtype=np.uint8)
        print(Image.open(buffer))
        print("opened")
        img = np.asarray(Image.open(buffer), dtype=np.uint8)
        print(img)
        #print(eval(_img))
        print("EVALED IMAGE\n\n\n")
        #dets = test_net_stream(net,img_dir + nm,thresh=0.05)
        dets = [[1,2,3,4,5,6,7] for i in range(21)]
        im = eval(_img)
        print("ABOUT TO EVAL\n\n\n\n\n")
        scores, boxes = im_detect(net, im, None)
        print(scores)

        x = repr(dets).replace("\n","").strip() ## parse detections for safe piping
        print("DID THE PARSING")
        #p.stdin.write(x+"\n")
            
    except:
        print("EXCEPTION\n\n\n")
