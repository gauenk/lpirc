# --------------------------------------------------------
# Fast/er R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Bharath Hariharan
# --------------------------------------------------------

import xml.etree.ElementTree as ET
import os
import cPickle
import scipy.io as sio
import numpy as np

def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text

        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    return objects

def _get_voc_results_file_template(devkit_path,image_set,year):
    # VOCdevkit/results/VOC2007/Main/<comp_id>_det_test_aeroplane.txt
    filename = 'stream0' + '_det_' + image_set + '_{:s}.txt'
    path = os.path.join(
        devkit_path,
        'results',
        'VOC' + year,
        'Main',
        filename)
    return path

def voc_ap(rec, prec):
    """ ap = voc_ap(rec, prec, [use_07_metric])
    Compute VOC AP given precision and recall.
    If use_07_metric is true, uses the
    VOC 07 11 point method (default:False).
    """
    use_07_metric = True
    if use_07_metric:
        # 11 point metric
        ap = 0.
        for t in np.arange(0., 1.1, 0.1):
            if np.sum(rec >= t) == 0:
                p = 0
            else:
                p = np.max(prec[rec >= t])
            ap = ap + p / 11.
    else:
        # correct AP calculation
        # first append sentinel values at the end
        mrec = np.concatenate(([0.], rec, [1.]))
        mpre = np.concatenate(([0.], prec, [0.]))

        # compute the precision envelope
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # to calculate area under PR curve, look for points
        # where X axis (recall) changes value
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # and sum (\Delta recall) * prec
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap

def voc_eval(det_lines,
             annopath,
             imagesetfile,
             classname,
             cachedir,
             ovthresh=0.5):
    """rec, prec, ap = voc_eval(detpath,
                                annopath,
                                imagesetfile,
                                classname,
                                [ovthresh])
    Top level function that does the PASCAL VOC evaluation.
    detpath: Path to detections
        detpath.format(classname) should produce the detection results file.
    annopath: Path to annotations
        annopath.format(imagename) should be the xml annotations file.
    imagesetfile: Text file containing the list of images, one image per line.
    classname: Category name (duh)
    cachedir: Directory for caching the annotations
    [ovthresh]: Overlap threshold (default = 0.5)
        (default False)
    """
    # assumes detections are in detpath.format(classname)
    # assumes annotations are in annopath.format(imagename)
    # assumes imagesetfile is a text file with each line an image name
    # cachedir caches the annotations in a pickle file

    # first load gt
    print(cachedir) #ImageNet: /home/gauenk/Documents/CAM2/image_team/faster_rcnn/frcnn_caffe/py-faster-rcnn/data/ImageNet/annotations_cache/annots.pkl
    if not os.path.isdir(cachedir):
        os.mkdir(cachedir)
    cachefile = os.path.join(cachedir, 'annots.pkl')
    # read list of images
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()
    if "ILSVRC" in imagesetfile:
        lines = [x.split(" ")[0] for x in lines]
    imagenames = [x.strip() for x in lines]
    if not os.path.isfile(cachefile):
        # load annots
        recs = {}
        for i, imagename in enumerate(imagenames):
            recs[imagename] = parse_rec(annopath.format(imagename))
            if i % 100 == 0:
                print 'Reading annotation for {:d}/{:d}'.format(
                    i + 1, len(imagenames))
        # save
        print 'Saving cached annotations to {:s}'.format(cachefile)
        with open(cachefile, 'w') as f:
            cPickle.dump(recs, f)
    else:
        # load
        with open(cachefile, 'r') as f:
            recs = cPickle.load(f)

    # extract gt objects for this class
    class_recs = {}
    npos = 0
    for imagename in imagenames:
        # for obj in recs[imagename]:
        #     print(obj)
        R = [obj for obj in recs[imagename] if obj['name'] == classname]
        bbox = np.array([x['bbox'] for x in R])
        #difficult = np.array([x['difficult'] for x in R]).astype(np.bool)
        det = [False] * len(R)
        npos = npos + len(R)
        class_recs[imagename] = {'bbox': bbox,
                                 #'difficult': difficult,
                                 'det': det}
    image_ids = [x[0] for x in det_lines]
    confidence = np.array([round(float(x[1]),3) for x in det_lines])
    BB = np.array([[round(float(z),1)+1 for z in x[2:]] for x in det_lines])
    # sort by confidence
    sorted_ind = np.argsort(-confidence)
    sorted_scores = np.sort(-confidence)
    if len(BB) == 0:
        return 0,0,0
    BB = BB[sorted_ind, :]
    image_ids = [image_ids[x] for x in sorted_ind]
    # print(sorted_scores[0:10])
    # print(sorted_scores[-10:-1])
    # print(image_ids[0:10])
    # print(image_ids[-10:-1])
    # print(np.max(confidence))
    # print(len([0 for i in confidence if i == float(1)]))
    # print(len([0 for i in confidence if i == float(0)]))
    # print(BB[0:3])
    # print(BB[-3:-1])
    # go down dets and mark TPs and FPs
    nd = len(image_ids)
    tp = np.zeros(nd)
    fp = np.zeros(nd)
    image_ids = [x.split(" ")[0] for x in image_ids]
    for d in range(nd):
        R = class_recs[image_ids[d]]
        bb = BB[d, :].astype(float)
        ovmax = -np.inf
        BBGT = R['bbox'].astype(float)
        if BBGT.size > 0:
            # compute overlaps
            # intersection
            ixmin = np.maximum(BBGT[:, 0], bb[0])
            iymin = np.maximum(BBGT[:, 1], bb[1])
            ixmax = np.minimum(BBGT[:, 2], bb[2])
            iymax = np.minimum(BBGT[:, 3], bb[3])
            iw = np.maximum(ixmax - ixmin + 1., 0.)
            ih = np.maximum(iymax - iymin + 1., 0.)
            inters = iw * ih

            # union
            uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
                   (BBGT[:, 2] - BBGT[:, 0] + 1.) *
                   (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)

            overlaps = inters / uni
            ovmax = np.max(overlaps)
            jmax = np.argmax(overlaps)

        if ovmax > ovthresh:
            #if not R['difficult'][jmax]:
            if not R['det'][jmax]:
                tp[d] = 1.
                R['det'][jmax] = 1
            else:
                fp[d] = 1.
        else:
            fp[d] = 1.

    # compute precision recall
    fp = np.cumsum(fp)
    tp = np.cumsum(tp)
    rec = tp / float(npos)
    # avoid divide by zero in case the first detection matches a difficult
    # ground truth
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)
    ap = voc_ap(rec, prec)
    if npos > 0:
        print(fp,tp,rec,prec,ap,npos)
    return rec, prec, ap


def _calc_map_(det_lines,year='2007'):
    image_set = "trainval"
    dataset = "VOC"
    devkit_path = "/home/gauenk/Documents/data/pascal_voc/VOCdevkit/"
    dataset_yr = dataset + year
    imageset_subdir = "Main"
    num_classes = 21

    output_dir = 'eval_output'
    imagesetfile = os.path.join(
        devkit_path,
        dataset_yr,
        "ImageSets",
        imageset_subdir,
        image_set + '.txt')
    annopath = os.path.join(
        devkit_path,
        dataset_yr,
        'Annotations',
        '{:s}.xml')
    if dataset == "ImageNet":
        synsets = sio.loadmat(os.path.join(devkit_path, 'meta_det.mat'))
        classes = ('__background__',)
        wnid = (0,)
        for i in xrange(200):
            classes = classes + (synsets['synsets'][0][i][2][0],)
            wnid = wnid + (synsets['synsets'][0][i][1][0],)
            wnid_to_ind = dict(zip(wnid, xrange(num_classes)))
            class_to_ind = dict(zip(classes, xrange(num_classes)))
    elif "VOC" in dataset:
        classes = ('__background__', # always index 0
                             'aeroplane', 'bicycle', 'bird', 'boat',
                             'bottle', 'bus', 'car', 'cat', 'chair',
                             'cow', 'diningtable', 'dog', 'horse',
                             'motorbike', 'person', 'pottedplant',
                             'sheep', 'sofa', 'train', 'tvmonitor')

    cachedir = os.path.join(devkit_path, 'annotations_cache')
    aps = []
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for i in range(1,len(det_lines)):
        cls = classes[i]
        if cls == '__background__' or cls == 0:
            continue
        if "ImageNet" in dataset:
            n_cls = wnid[i]
        else:
            n_cls = cls
        filename = _get_voc_results_file_template(devkit_path,image_set,year).format(cls)
        rec, prec, ap = voc_eval(
            det_lines[i], annopath, imagesetfile, n_cls, cachedir, ovthresh=0.5)
        aps += [ap]
        print('AP for {} = {:.4f}'.format(cls, ap))
        with open(os.path.join(output_dir, str(cls) + '_pr.pkl'), 'w') as f:
            cPickle.dump({'rec': rec, 'prec': prec, 'ap': ap}, f)
    print('Mean AP = {:.4f}'.format(np.mean(aps)))
    print('~~~~~~~~')
    print('Results:')
    for ap in aps:
        print('{:.3f}'.format(ap))
    print('{:.3f}'.format(np.mean(aps)))
    print('~~~~~~~~')
    print('')
    print('--------------------------------------------------------------')
    print('Results computed with the **unofficial** Python eval code.')
    print('Results should be very close to the official MATLAB eval code.')
    print('Recompute with `./tools/reval.py --matlab ...` for your paper.')
    print('-- Thanks, The Management')
    print('--------------------------------------------------------------')
