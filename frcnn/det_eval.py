import _init_paths
from stream_eval import _calc_map_
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list
from datasets.factory import get_imdb
from fast_rcnn.nms_wrapper import nms
import caffe
import cPickle
import os,sys,urllib2

def load_image_set():
    with open("/home/gauenk/Documents/data/pascal_voc/VOCdevkit/VOC2007/ImageSets/Main/trainval.txt","r") as f:
        lines = f.readlines()
    return [x.strip() for x in lines]


out_dir = "./out_dir/"

## TEST
#VOC 2007
#det_file = "../../output/faster_rcnn_end2end/voc_2007_trainval/VGG16_faster_rcnn_final/detections.pkl"

#ImageNet_short_train
det_file = "/home/gauenk/Documents/CAM2/image_team/faster_rcnn/frcnn_caffe/py-faster-rcnn/output/faster_rcnn_end2end/imagenet_short_train/VGG16.v2/detections.pkl"

def write_boxes(dets,fn,cls):
    f = open("./out_dir/" + fn + "_" + str(cls) + "_" + ".txt", 'w')
    for idx in range(1,len(dets[cls])):
        for i in dets[cls][idx]:
            f.write( cls + " " + str(idx) + " " + str(i[-1]))
            for j in range(len(i)-1):
                f.write(" " + str(i[j]))
            f.write("\n")


def apply_nms(all_boxes, thresh):
    """Apply non-maximum suppression to all predicted boxes output by the
    test_net method.
    """
    num_classes = len(all_boxes)
    num_images = len(all_boxes[0])
    nms_boxes = [[[] for _ in xrange(num_images)]
                 for _ in xrange(num_classes)]
    for cls_ind in xrange(num_classes):
        for im_ind in xrange(num_images):
            dets = all_boxes[cls_ind][im_ind]
            if dets == []:
                continue
            # CPU NMS is much faster than GPU NMS when the number of boxes
            # is relative small (e.g., < 10k)
            # TODO(rbg): autotune NMS dispatch
            keep = nms(dets, thresh, force_cpu=True)
            if len(keep) == 0:
                continue
            nms_boxes[cls_ind][im_ind] = dets[keep, :].copy()
    return nms_boxes


with open(det_file,"r") as f:
    recs = cPickle.load(f)
tlist = load_image_set()
nms_dets = apply_nms(recs, cfg.TEST.NMS)
nlist =[ [ [ [tlist[i], " ",] + [z[-1]] + list(z[0:4]) for z in j[i]]  for i in range(len(j))] for j in nms_dets]
alist =[ [k for z in j for k in z] for j in nlist ]
print(alist)
_calc_map_(alist)
## TEST


# mlist = os.listdir(out_dir)
# nclasses = 21
# for i in mlist:
#     with open(out_dir + i,"r") as f:
#         lines = f.readlines()
#     d = [[l.split()[0]] + [float(l.split()[k]) for k in range(len(l.split())) if k != 0] for l in lines]
#     ocls = [[] for i in range(nclasses)]
#     for z in range(1,nclasses+1):
#         ocls[z-1] = [j for j in d if int(j[1]) == z]
#     print(len(ocls))
#     print(len(ocls[0]))
#     print(len(ocls[1]))
#     print(len(ocls[2]))
#     print(ocls[1][0])
#     print(ocls[1][0][1])
#     _calc_map_(ocls)
