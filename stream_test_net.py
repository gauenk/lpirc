import _init_paths
from test_stream_lib import test_net_stream
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list
from datasets.factory import get_imdb
import caffe
import cPickle
import os,sys,urllib2

def send_dets(dets,img_id,fn):
    f = open("./out_dir/" + fn + ".txt", 'a')
    for idx in range(1,len(dets)):
        for i in dets[idx][0]:
            f.write(img_id + " " + str(idx) + " " + str(i[-1]))
            for j in range(len(i)-1):
                f.write(" " + str(i[j]))
            f.write("\n")

def load_image_set():
    #filen = "/home/gauenk/Documents/data/pascal_voc/VOCdevkit/VOC2007/ImageSets/Main/trainval.txt"
    filen = "/home/gauenk/Documents/CAM2/image_team/faster_rcnn/frcnn_caffe/py-faster-rcnn/tools/lpirc/anup/adithya"
    with open(filen,"r") as f:
        lines = f.readlines()
    return [x.strip() for x in lines]

base_fold = "/home/gauenk/Documents/CAM2/image_team/faster_rcnn/frcnn_caffe/py-faster-rcnn/tools/lpirc/anup"
#sub_fold = ["adithya", "cam2","inria"]
#per_fold = ["10%","25%","30%","40%","50%","75%","100%"]
sub_fold = ["inria"]
per_fold = ["100%"]

cfg.GPU_ID = 0
caffe.set_mode_gpu()
caffe.set_device(0)
t_prototxt = "test.prototxt"
caffemodel = "VGG16_faster_rcnn_final.caffemodel"
net = caffe.Net(t_prototxt, caffemodel, caffe.TEST)
net.name = os.path.splitext(os.path.basename(caffemodel))[0]

for i in sub_fold:
    for j in per_fold:
        print(i,j)
        path = os.path.join(base_fold,i,j)
        nlist = os.listdir(path)
        mlist = [l for l in nlist if ".png" in l]
        num_imgs = len(mlist)
        for k in range(num_imgs):
            print(i,j,mlist[k])
            print("{}/{}".format(k,num_imgs))
            dets = test_net_stream(net,os.path.join(path,mlist[k]))
            send_dets(dets, mlist[k], "_" + str(i) + "_" + str(j) + "_")
        
# img_dir = "/home/gauenk/Documents/data/pascal_voc/VOCdevkit/VOC2007/JPEGImages/"
# mlist = load_image_set()
# num_imgs = len(mlist)
# for i in range(len(mlist)):
#     print("{}/{}".format(i,num_imgs))
#     dets = test_net_stream(net,img_dir + mlist[i] + ".jpg")
#     send_dets(dets, mlist[i])
#     #os.remove(img_dir + mlist[0])






