#renames TE files to .te extention
L = []
index = open("TE_filenames.txt","r")
for line in index:
    print("working",line)
    line2 = line.strip().split("_sorted.out")[0]+".te"
    F1 = open("TE_ids/"+line.strip(),"r")
    F2 = open("TE_ids/"+line2,"w")
    F2.write(F1.read())
    F1.close()
    F2.close()
    print("done",line)
index.close()
