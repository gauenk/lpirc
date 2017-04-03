import os,sys
import _init_paths,thread
import caffe
import numpy as np
from test_stream_lib import test_net_stream
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list
from datasets.factory import get_imdb
from send_dets import send_dets
from signal import SIGTERM as sig_sgtm

def detect_images(net,time_to_live,post_data):
    import multiprocessing as mp
    import os,sys,time
    import _init_paths
    import caffe
    import subprocess
    import atexit
    p = subprocess.Popen(['python', 'test.py'], stdin = subprocess.PIPE)
    p.stdin.write(repr(post_data)+"\n")
    #print("\n\nDET IMAGES SEND POST DATA")
    #mp.set_start_method('spawn')
    caffe.set_mode_gpu()
    caffe.set_device(0)
    ## post_data = [token,host_data]
    img_dir = "./images/"
    mlist = os.listdir(img_dir)
    n_classes= 21
    pr_list = []
    n_time = time.time()
    print("IN DET")
    while(time_to_live > 0):
        if len(mlist) > 0:
            nm = mlist[0]
            det_dict = {'image_name': nm}
            print(time.time() - n_time)
            dets = test_net_stream(net,img_dir + nm,thresh=0.05)
            x = repr(dets)
            x = x.replace("\n","")
            x = x.strip()
            p.stdin.write(x+"\n")
            time.sleep(1)
            n_time = time.time()
            os.remove(img_dir + nm)
            #time_to_live -= 1
        mlist = os.listdir(img_dir)
        atexit.register(p.kill)





def pipe_detect_images(net,time_to_live,post_data):
    import os,sys,time
    import _init_paths
    import caffe
    import subprocess
    import atexit
    p = subprocess.Popen(['python', 'test.py'], stdin = subprocess.PIPE)
    p.stdin.write(repr(post_data)+"\n")
    caffe.set_mode_gpu()
    caffe.set_device(0)
    #img_dir = "./images/"
    #mlist = os.listdir(img_dir)
    n_classes= 21
    pr_list = []
    n_time = time.time()

    print("IN DET")

    while(time_to_live > 0):
        try:
            _img = raw_input()
            print("GOT IMAGE\n\n")
            print(_img)
            print(eval(_img))
            print("EVALED IMAGE\n\n\n")
        except:
            print("EXCEPTION\n\n\n")
        
        # if len(mlist) > 0:
        #     nm = mlist[0]
        #     det_dict = {'image_name': nm}
        #     print(time.time() - n_time)
        #     dets = test_net_stream(net,img_dir + nm,thresh=0.05)
        #     x = repr(dets)
        #     x = x.replace("\n","")
        #     x = x.strip()
        #     p.stdin.write(x+"\n")
        #     time.sleep(1)
        #     n_time = time.time()
        #     os.remove(img_dir + nm)
        #     #time_to_live -= 1
        # mlist = os.listdir(img_dir)
        # atexit.register(p.kill)




