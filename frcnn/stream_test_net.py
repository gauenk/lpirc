import os,sys
import _init_paths,thread
import caffe
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
    mp.set_start_method('spawn')
    print("INHERE")
    caffe.set_mode_gpu()
    print("SETMODEGPU")
    caffe.set_device(0)
    print("POSTCAFFESET")
    ## post_data = [token,host_data]
    img_dir = "./images/"
    mlist = os.listdir(img_dir)
    pr_list = []
    n_time = time.time()
    print("IN DET")
    while(time_to_live > 0):
        if len(mlist) > 0:
            nm = mlist[0]
            print(time.time() - n_time)
            dets = test_net_stream(net,img_dir + nm,thresh=0.05)
            n_time = time.time()
            a = mp.Process(target=send_dets,args=(dets, nm,post_data),daemon=True)
            a.start()
            os.remove(img_dir + nm)
            #time_to_live -= 1
        mlist = os.listdir(img_dir)





