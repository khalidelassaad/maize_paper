#A program to split the sorted TE list into subfiles
#by their ref id (column 0) and stores the output
#files in the TE_ids dir
import updater
import time
F = open("TE_annotations.gff3","r")
D = {}
JU = 0
X = 0
while True:
    now = time.time()
    if not int(now)%5:
        if not JU:
            rs = ""
            for key in D:
                rs += key + " " + str(D[key][1]) + "\n"
            updater.updater("Lines read {}/{}".format(X,201762),rs,"Percent complete {:.2f}%".format(X/201762*100))
            JU = 1
    else:
        JU = 0
    L = F.readline()
    if not L:
        break
    name = L.split("\t")[0]
    if not name in D:
        D[name] = [open("TE_ids/"+name+".te","w"),0]
    D[name][0].write(L)
    D[name][1] += 1
    X += 1

F.close()
for key in D:
    D[key][0].close()
