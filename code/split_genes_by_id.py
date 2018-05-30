#A program to split the sorted gene list into subfiles
#by their ref id (column 0) and stores the output
#files in the GENE_ids dir
import updater
import time
F = open("Gene_annotations_sorted.gff3","r")
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
            updater.updater("Lines read {}/{}".format(X,2908539),rs,"Percent complete {:.2f}%".format(X/2908539*100))
            JU = 1
    else:
        JU = 0
    L = F.readline()
    if not L:
        break
    name = L.split("\t")[0]
    if not name in D:
        D[name] = [open("GENE_ids/"+name+".gene","w"),0]
    D[name][0].write(L)
    D[name][1] += 1
    X += 1

F.close()
for key in D:
    D[key][0].close()
