#merges sorted blast .outs together, zips them up
import subprocess 

WORKINGDIR = "sorted_blasts/"

def getfiles():
    "Returns an array of filenames from the sorted_blasts/ directory"
    proc = subprocess.Popen(["ls",WORKINGDIR], stdout=subprocess.PIPE)
    returnfiles = []
    for entry in proc.stdout:
        returnfiles.append(entry.decode("utf-8").strip())
    return returnfiles

def maketuple(line):
    splitline = line.split("\t")
    index = min(int(splitline[8]),int(splitline[9]))
    return (index,line)

class BlastFile:
    def __init__(self,filename):
        self.filename = filename
        self.index = 0
        self.line = ""
        self.EOF = False

    def openfile(self):
        self.infile = open(WORKINGDIR+self.filename,"r")
        return

    def closefile(self):
        self.infile.close()
        return

    def readnextline(self):
        if self.EOF:
            raise KeyError
        templine = self.infile.readline()
        if not templine:
            self.EOF = True
        else:
            self.line = templine
            splitline = self.line.split("\t")
            self.index = min(int(splitline[8]),int(splitline[9]))
        return
"""
B = BlastFile(getfiles()[0])
B.openfile()
writefile = open("TEST.out","w")
for x in range(5):
    B.readnextline()
    writefile.write(B.line)
writefile.close()
B.closefile()
"""
writefile = open("maizegenome_ALLBLASTS_SORTED.out","w")
files = getfiles()
filelist = []
for entry in files:
    filelist.append(BlastFile(entry))
for B in filelist:
    B.openfile()
    B.readnextline()

while filelist:
    filelist.sort(key=lambda B: B.index)
    B = filelist[0]
    if B.EOF:
        filelist = filelist[1:]
        B.closefile()
        continue
    writefile.write(B.line)
    B.readnextline()




for B in filelist:
    B.closefile()
writefile.close()












