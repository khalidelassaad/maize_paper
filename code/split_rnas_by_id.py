#A program to split the sorted RNA list into subfiles
#by their ref id (column 1) and stores the output
#files in the RNA_ids dir
import updater
import time
F = open("maizegenome_ALLBLASTS_SORTED.out","r")
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
            updater.updater("Lines read {}/{}".format(X,796026151),rs,"Percent complete {:.2f}%".format(X/796026151*100))
            JU = 1
    else:
        JU = 0
    L = F.readline()
    if not L:
        break
    name = L.split("\t")[1]
    if not name in D:
        D[name] = [open("RNA_ids/"+name+".rna","w"),0]
    D[name][0].write(L)
    D[name][1] += 1
    X += 1

F.close()
for key in D:
    D[key][0].close()
