import os,sys,re

def readCSV(fn):
    with open(fn,"r") as f:
        lines = f.readlines()
    return lines

def load_dict():
    voc_dir = "/home/gauenk/Documents/data/VOCdevkit/VOC2007/JPEGImages"
    lines = readCSV("/home/gauenk/rename_voc_2007.csv")

    voc_list = os.listdir(voc_dir)
    voc_list = [i.split(".")[0] for i in voc_list]
    nlist = [i.split(".")[0] for i in lines][0:-1] # get rid of "_list"
    mlist = [re.findall(r"[0-9]+",lines[i].split(".")[2])[0] for i in range(len(lines)-1)]
    mdict = {}
    for i in range(len(mlist)):
        mdict[int(float(mlist[i]))] = str(nlist[i])
    return mdict

if __name__ == "__main__":
    m = load_dict()
    print(m[5011])
