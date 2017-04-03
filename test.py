import ast
import time,re
from numpy import array, all, float32
from send_dets import send_dets

dets = []
img_names = [0]
post_data = None
while(True):
    try:
        line = raw_input() 
        if post_data is None:
            post_data = eval(line)
            continue
        det = eval(line)
        dets += det
        img_names += [img_names[-1] + 1]
        if len(dets) > 1:
            send_dets(dets,img_names,post_data)
        time.sleep(5)
    except EOFError:
        print("EOF: Exeception")
        time.sleep(0.1)
    except:
        print("OTHER: Exeception")
        raise

