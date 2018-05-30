#This script finds gene alignments from the sorted blast that
#overlap with a TE at one point or another
import time

MAX_READ_LENGTH = 9302 #found manually from sorted reads file
DEBUG = 0

if DEBUG:
    dprint = print
else:
    def dprint(*args):
        return

class ReadList:
    def __init__(self, filename, col1, col2):
        self.filename = filename
        self.F = open(filename)
        print("Opened",filename)
        if col1 >= col2:
            raise ValueError
        self.col1 = col1
        self.col2 = col2
        self.L = []
        self.EOF = False #becomes true once end of file is
                         #reached. Addline won't do anything

    def __del__(self):
        self.F.close()
        print("Closed",self.filename)

    def __str__(self):
        rs = ""
        for line in self.L:
            rs += str(line)+"\n"
        return rs

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.L)

    def addline(self):
        if self.EOF:
            return
        l = self.F.readline()
        currpos = self.F.tell()
        if not self.F.readline():
            self.EOF = True
        self.F.seek(currpos)
        line = l.split("\t")
        x = min(int(line[self.col1]),int(line[self.col2]))
        y = max(int(line[self.col1]),int(line[self.col2]))
        self.L.append((x,y,l))
        return (x,y,l)

    def popline(self):
        if not self.L:
            return
        rt = self.L[0]
        self.L = self.L[1:]
        return rt

    def popall(self):
        self.L = []
        return

    def pop(self,key):
        return self.L.pop(key)

    def __getitem__(self,key):
        try:
            return self.L[key]
        except IndexError:
            if key < 0:
                raise IndexError
            for x in range(key-len(self.L)+1):
                self.addline()
            return self.L[key]

def lines_up(x1, y1, x2, y2):
    """Given a start position and an end position of 2 sequences,
    determines their alignment
    0 - No alignment
    1 - Partial alignment (even a one base alignment counts)
    2 - First totally encapsulated by second
    3 - Second totally encapsulated by first
    4 - First and second exactly match
    5 - error
    """
    if x1 == x2 and y1 == y2:
        return 4
    if x1 <= x2 and y1 >= y2:
        return 3
    if x1 >= x2 and y1 <= y2:
        return 2
    if (x2 <= x1 and x1 <= y2) or (x2 <= y1 and y1 <= y2):
        return 1
    if y1 < x2 or y2 < x1:
        return 0
    return 5

class TE_RNA_Aligner:
    def __init__(self, TE_name, RNA_name,writefile_name):
        self.TE = ReadList(TE_name,3,4)
        self.RNA = ReadList(RNA_name,8,9)
        self.writefile = open(writefile_name,"w")
        self.writefile_name = writefile_name
        print("Opened",writefile_name)

    def __del__(self):
        self.writefile.close()
        print("Closed",self.writefile_name)

    def output(self,RNAline,TEline,an):
        rs = RNAline.strip() + "\t" + TEline.strip() + "\t" + str(an) + "\n"
        self.writefile.write(rs)    
        return

    def run(self):
        RNAdex = 0
        TEdex = 0
        aligns = 0
        ju = 0
        while (not self.TE.EOF) or len(self.TE):
            while not(self.RNA.EOF) or len(self.RNA):
                if len(self.RNA) == RNAdex and self.RNA.EOF:
                    return aligns
                RNAline = self.RNA[RNAdex]
                try:
                    TEline = self.TE[0]
                except IndexError:
                    return aligns
                r1,r2,t1,t2 = RNAline[0],RNAline[1],TEline[0],TEline[1]
                now = time.time()
                if not int(now) % 5:
                    if not ju:
                        ts = time.strftime('%H:%M:%S',time.localtime(now))
                        print("Update at",ts)
                        print("Filename:",self.writefile_name)
                        print("Aligns found",aligns)
                        print("RNAlen",len(self.RNA))
                        print("TElen ",len(self.TE))
                        print("processing",r1,r2,t1,t2)
                        print("TEs processed: {}".format(TEdex))
                        print()
                        ju = 1
                else:
                    ju = 0

                dprint("processing",r1,r2,t1,t2)
                if r1 > t2:
                    RNAdex = 0
                    self.TE.popline()
                    TEdex += 1
                    break
                if r2 < t1:
                    self.RNA.pop(RNAdex)
                    dprint("pop",RNAdex)
                    continue
                #Output
                aligns = aligns + 1
                dprint("    aligns",r1,r2,t1,t2)
                an = lines_up(t1,t2,r1,r2)
                self.output(RNAline[2],TEline[2],an)
                if not self.RNA.EOF:
                    RNAdex = RNAdex + 1
                elif RNAdex + 1 < len(self.RNA):
                    RNAdex = RNAdex + 1
                else:
                    RNAdex = 0
                    self.TE.popline()
                    TEdex += 1
            if self.RNA.EOF and not len(self.RNA):
                break
        return aligns
"""
    def run(self): #THE MONEY FUNCTION
        RNAdex = 0
        TEdex = 0
        while True:
            RNAline = self.RNA[RNAdex]
            TEline = self.TE[TEdex]
            r1,r2,t1,t2 = RNAline[0],RNAline[1],TEline[0],TEline[1]
            if r1 < t1:
                if r2 >= t1:
                    an = lines_up(t1,t2,r1,r2)
                    #output
                    self.output(RNAline[2],TEline[2],an)
                    if self.RNA.EOF and RNAdex == len(self.RNA) - 1:
                        self.TE.popline()
                        RNAdex = 0
                    else:
                        RNAdex += 1
                else:
                    if RNAdex == 0:
                        self.RNA.popline()
                    else:
                        if self.RNA.EOF and RNAdex == len(self.RNA) - 1:
                            self.TE.popline()
                            RNAdex = 0
                        else:
                            RNAdex += 1
            else:
                if r1 <= t2:
                    an = lines_up(t1,t2,r1,r2)
                    #output
                    self.output(RNAline[2],TEline[2],an)
                    if self.RNA.EOF and RNAdex == len(self.RNA) - 1:
                        self.TE.popline()
                        RNAdex = 0
                    else:
                        RNAdex += 1
                else:
                    self.TE.popline()
                    RNAdex = 0
                    continue
            if self.RNA.EOF and RNAdex == len(self.RNA) - 1:
                self.TE.popline()
            if self.RNA.EOF and self.TE.EOF and len(self.TE) == 0:
                break
        return
"""
#TE = ReadList("TEtest.gff3",3,4)
#RNA = ReadList("RNAtest.out",8,9)

#a = TE_RNA_Aligner("TEtest.gff3","RNAtest.out","testoutput.txt")
#a = TE_RNA_Aligner("TEtest2.gff3","RNAtest2.out","testoutput.txt")
#a = TE_RNA_Aligner("TE_annotations_sorted.gff3","maizegenome_ALLBLASTS_SORTED.out","testoutput.txt")
#a = TE_RNA_Aligner("TE_1_sorted.gff3","maizegenome_ALLBLASTS_SORTED.out","testoutput.txt")

#print(a.run())

