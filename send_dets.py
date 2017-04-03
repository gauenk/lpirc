import os,sys
from urllib import urlencode
import pycurl
from collections import defaultdict

def run(token,data,host_data,dtype):
    send_post_data(token,data,host_data,dtype)    

def send_dets(dets,fns,post_data):

    l = defaultdict(list)
    for fn in fns:
        img_nm = fn
        for idx in range(1,len(dets)):
            for jdx in range(len(dets[idx])):
                for i in dets[idx][jdx]:
                    l[0].append(img_nm)
                    l[1].append(idx)
                    l[2].append(i[-1])
                    l[3].append(i[0])
                    l[4].append(i[1])
                    l[5].append(i[2])
                    l[6].append(i[3])

    pdict = {'image_name':l[0],\
             'CLASS_ID':l[1],\
             'confidence':l[2],\
             'xmin':l[3],\
             'ymin':l[4],\
             'xmax':l[5],\
             'ymax':l[6],\
    }
    if send_post_data(post_data[0],pdict,post_data[1:],"result") == 0:
        print("posting failed")
        return 0
    print("sent dets")
    return 1
            
def send_post_data(token,data,host_data,dtype):
    c = pycurl.Curl()
    c.setopt(c.URL, host_data[0] +':'+host_data[1]+'/' + dtype)
    post_data = {'token':token}
    postfields = urlencode(post_data)+'&'+urlencode(data,True)
    c.setopt(c.POSTFIELDS,postfields)
    c.perform()
    status = c.getinfo(pycurl.HTTP_CODE)
    c.close()
    if status == 200:
        # Server replied 200, OK, Result stored
        return 1
    else:
        # Server replied 401, Unauthorized Access
        print "Unauthorized Access\n"
        return 0

if __name__ == "__main__":
    send_dets(dets,fn,post_data)
    run(sys.argv[0],sys.argv[1],sys.argv[3],sys.argv[4])
