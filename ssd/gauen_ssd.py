import _init_paths
import caffe
import numpy as np
import pprint
import time, os, sys
import cv2,time

def im_list_to_blob(ims):
    """Convert a list of images into a network input.

    Assumes images are already prepared (means subtracted, BGR order, ...).
    """
    max_shape = np.array([im.shape for im in ims]).max(axis=0)
    num_images = len(ims)
    blob = np.zeros((num_images, max_shape[0], max_shape[1], 3),
                    dtype=np.float32)
    for i in xrange(num_images):
        im = ims[i]
        blob[i, 0:im.shape[0], 0:im.shape[1], :] = im
    # Move channels (axis 3) to axis 1
    # Axis order will become: (batch elem, channel, height, width)
    channel_swap = (0, 3, 1, 2)
    blob = blob.transpose(channel_swap)
    return blob

def _get_image_blob(im):
    """Converts an image into a network input.

    Arguments:
        im (ndarray): a color image in BGR order

    Returns:
        blob (ndarray): a data blob holding an image pyramid
        im_scale_factors (list): list of image scales (relative to im) used
            in the image pyramid
    """
    im_orig = im.astype(np.float32, copy=True)
    im_orig -= np.array([[[102.9801, 115.9465, 122.7717]]]) #cfg.PIXEL_MEANS

    im_shape = im_orig.shape
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])

    processed_ims = []
    im_scale_factors = []

    target_sizes = [300]
    for target_size in target_sizes:
        im_scale = float(target_size) / float(im_size_min) #kent commented
        im_scale_x = float(300) / float(im_shape[1])
        im_scale_y = float(300) / float(im_shape[0])
        im = cv2.resize(im_orig, None, None, fx=im_scale_x, fy=im_scale_y,
                        interpolation=cv2.INTER_LINEAR)
        im_scale_factors.append(im_scale)
        processed_ims.append(im)

    # Create a blob to hold the input images
    blob = im_list_to_blob(processed_ims)
    return blob, np.array(im_scale_factors)

def _get_blobs(im, rois):
    """Convert an image and RoIs within that image into network inputs."""
    blobs = {'data' : None, 'rois' : None}
    blobs['data'], im_scale_factors = _get_image_blob(im)
    return blobs, im_scale_factors

img_dir = "/home/ubuntu/Documents/py-faster-rcnn/tools/lpirc/images/"
prototxt = "models/VGGNet/VOC0712Plus/SSD_300x300_ft/deploy.prototxt"
caffemodel = "models/VGGNet/VOC0712Plus/SSD_300x300_ft/VGG_VOC0712Plus_SSD_300x300_ft_iter_160000.caffemodel"

caffe.set_mode_gpu()
caffe.set_device(0)
net = caffe.Net(prototxt, caffemodel, caffe.TEST)
net.name = os.path.splitext(os.path.basename(caffemodel))[0]
mlist = os.listdir(img_dir)
boxes = None
batchsize = 1
t_end = time.time() + 60
while(t_end > time.time()):
    print(t_end - time.time())
    i = 0
    if(len(mlist) > 0):
        print("here")
        b_im = np.empty([batchsize,3,300,300])
        for j in range(batchsize):
            filename = mlist[batchsize*i:batchsize*i+j+1][0]
            im,im_scales = _get_image_blob(cv2.imread(img_dir + filename))
            b_im[j] = im
        blobs = {'data' : None, 'rois' : None}
        blobs['data'] = b_im
        net.blobs['data'].reshape(*(blobs['data'].shape))
        forward_kwargs = {'data': b_im.astype(np.float32, copy=False)}
        blobs_out = net.forward(**forward_kwargs)
        # not necessary for lpirc eval.. for me to eval and verify correct operation
        for l in range(batchsize):
            filename = mlist[batchsize*i:batchsize*i+l+1][0]
            indx = [k for k in range(blobs_out['detection_out'].shape[2]) if int(blobs_out['detection_out'][0,0,k,0]) == l ]
            for k in indx:
                blobs_out['detection_out'][0,0,k,0] = int(filename.split(".")[0])
        print(blobs_out.keys())
        print(blobs_out['detection_out'].shape)
        print(blobs_out['detection_out'][0][0].shape)
        print(blobs_out['detection_out'][0,0,:,0].shape)
        print(blobs_out['detection_out'][0][0][0][:].shape)
        print(np.max(blobs_out['detection_out'][0,0,:,0]))
        print(np.max(blobs_out['detection_out'][0,0,:,1]))
         

    mlist = os.listdir(img_dir)
    
