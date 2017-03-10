import os,sys
from urllib import urlencode
import pycurl

def run(token,data,host_data,dtype):
    send_post_data(token,data,host_data,dtype)    

def save_dets(dets,fn):
    f = open("./out_dir/" + fn[:-4] + ".txt", 'a')
    for idx in range(1,len(dets)):
        for i in dets[idx][0]:
            f.write(fn[:-4] + " " + str(idx) + " " + str(i[-1]))
            for j in range(len(i)-1):
                f.write(" " + str(i[j]))
            f.write("\n")

def send_dets(dets,fn,post_data):
    ## host_data = [host_ipaddress,host_port]
    f = open("./out_dir/" + fn[:-4] + ".txt", 'a')
    img_nm = fn.split(".")[0]

    for idx in range(1,len(dets)):
        for i in dets[idx][0]:
            pdict = {'image_name':img_nm,\
                     'CLASS_ID':idx,\
                     'confidence':i[-1],\
                     'xmin':i[0],\
                     'ymin':i[1],\
                     'xmax':i[2],\
                     'ymax':i[3],\
            }
            if send_post_data(post_data[0],pdict,post_data[1:],"result") == 0:
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
