#!/usr/bin/env python2
## FOR FRCNN
import _init_paths
from test_stream_lib import test_net_stream
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list
from datasets.factory import get_imdb
import caffe
import cPickle
import atexit,thread
from signal import SIGTERM as sig_sgtm

## ELSE
from multiprocessing import Process
import os,sys,urllib2
sys.path.insert(0, 'LPIRC/client/source/')
from client import *
from get_image_files import run_get_images
from stream_test_net import detect_images


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    print("BOTH STARTED")
    for p in proc:
        p.join()

##SET UP CLIENT
#+++++++++++++++++++++++++++ Global Variables ++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++ Start of the script +++++++++++++++++++++++++++++++++++++++++++++++

##SET UP STREAM_TEST_NET
cfg.GPU_ID = 0
t_prototxt = "/home/ubuntu/Documents/py-faster-rcnn/models/pascal_voc/ZF/faster_rcnn_end2end/test.prototxt"
caffemodel = "/home/ubuntu/Documents/py-faster-rcnn/weights/pascal_voc/ZF_faster_rcnn_final.caffemodel"

net = caffe.Net(t_prototxt, caffemodel, caffe.TEST)
net.name = os.path.splitext(os.path.basename(caffemodel))[0]


## LOGIN AND GET TOKEN
parse_cmd_line()
[token, status] = get_token(username,password)   # Login to server and obtain token
if status==0:
    print "Incorrect Username and Password. Bye!"
    sys.exit()



## start the process to recieve images
run_get_images(token,image_directory,net)

#p_get_imgs = subprocess.Popen(['python', 'test.py'], stdin = subprocess.PIPE)
## start the process to detection images
## opened in p_get_imgs
##p_get_dets = subprocess.Popen(['python', 'get_detections.py'], stdin = subprocess.PIPE)

## start the process to send detections
## opened in p_get_dets
#p_send_dets = subprocess.Popen(['python', 'test.py'], stdin = subprocess.PIPE)

#a = Process(target=run_get_images,args=(token,image_directory))
#a.start()
#ttl = 1000
#detect_images(net,ttl,[token,"192.168.1.2","5033"])


while True:
    pass
#post_logout (token)

