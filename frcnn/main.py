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

ttl = 1000

a = Process(target=run_get_images,args=(token,image_directory))
a.start()
detect_images(net,ttl,[token,"192.168.1.2","5006"])

while True:
    pass
#post_logout (token)

