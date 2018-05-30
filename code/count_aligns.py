#A program that counts the different types of overlaps
#in the overlap output file
import time
index = open("overlap_files.txt","r")
D = {}
JU = 0
X = 0
for filename in index:
    filename = filename.strip()
    writefilename = "overlaps/"+filename.split(".out")[0]+".count"
    filename = "overlaps/"+filename
    F = open(filename,"r")
    WF = open(writefilename,"w")
    while True:
        L = F.readline()
        if not L:
            break
        try:
            D[L.strip().split("\t")[-1]] += 1
        except KeyError:
            D[L.strip().split("\t")[-1]] = 1
        now = time.time()
        if not int(now)%5:
            if not JU:
                ts = time.strftime('%H:%M:%S',time.localtime(now))
                print("Update at",ts)
                print("Filename",filename)
                print("Line {}".format(X))
                print(D)
                print()
                JU = 1
        else:
            JU = 0
        X+=1
    WF.write("Overlap types:\n"+str(D)+"\nNumber of lines:"+str(X))
    D = {}
    X = 0
    WF.close()
    F.close()
index.close()
print("Done")

