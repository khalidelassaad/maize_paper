## AUTHOR: Khalid Elassaad
import sys

def size_list_and_elements(L):
    #Gets size in bytes of a List of elements
    sizesum = sys.getsizeof(L)
    for item in L:
        sizesum += sys.getsizeof(item)
    return sizesum

class ReadList:
    #ReadList class for space efficient file I/O
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

    def addall(self):
        while self.addline():
            continue
        return

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
        # Overloads indexing [] operator, adds lines automatically
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




class Aligner:
    # Runs an overlap detection on two tab separated files, given filenames and column numbers
    def __init__(self, FILE1_name, FILE1_col1, FILE1_col2, FILE2_name, FILE2_col1, FILE2_col2,writefile_name):
        self.FILE1 = ReadList(FILE1_name,FILE1_col1,FILE1_col2)
        self.FILE2 = ReadList(FILE2_name,FILE2_col1,FILE2_col2)
        self.writefile = open(writefile_name,"w")
        self.writefile_name = writefile_name
        print("Opened",writefile_name)

    def __del__(self):
        try:
            self.writefile.close()
            print("Closed",self.writefile_name)
        except:
            pass

    def overload(self):
        self.FILE1.addall()
        self.FILE2.addall()
        return

    def output(self,FILE2line,FILE1line,an):
        rs = FILE2line.strip() + "\t" + FILE1line.strip() + "\t" + str(an) + "\n"
        self.writefile.write(rs)    
        return

    def run(self):
        #Runs the overlap detction algorithm
        FILE1dex = 0 #How far into FILE1 we are
        aligns = 0 #total number of alignments found

        while True:
            try: ## Load from file 1
                line1 = self.FILE1[FILE1dex]
                l1start = line1[0]
                l1end   = line1[1]
            except IndexError:
                if FILE1dex == 0:
                    break
                else:
                    FILE1dex = 0
                    self.FILE2.pop(0)
                    continue

            try: ## Load from file 2
                line2 = self.FILE2[0]
                l2start = line2[0]
                l2end   = line2[1]
            except IndexError:
                break

            if l1start > l2end:
                FILE1dex = 0
                self.FILE2.pop(0)
                continue

            if l2start > l1end:
                self.FILE1.pop(0)
                continue

            ## Once this point is reached, an overlap has been found!
            aligns = aligns + 1
            alignment_number = lines_up(l2start, l2end, l1start, l1end)
            self.output(line2[2], line1[2], alignment_number)
            FILE1dex += 1

        ## Close outputs
        del(self.FILE1)
        del(self.FILE2)
        self.writefile.close()
        print("Closed",self.writefile_name)

        return aligns

    def run_with_space_analysis(self, outfile):
        #Runs the overlap detection algorithm AND writes space usage to a log file for later analysis
        FILE1dex = 0 #How far into FILE1 we are
        aligns = 0 #total number of alignments found
        log = open(outfile, "w")
        while True:
            sizeL1 = size_list_and_elements(self.FILE1.L)
            sizeL2 = size_list_and_elements(self.FILE2.L)
            log.write("{} {}\n".format(sizeL1,sizeL2))
            try: ## Load from file 1
                line1 = self.FILE1[FILE1dex]
                l1start = line1[0]
                l1end   = line1[1]
            except IndexError:
                if FILE1dex == 0:
                    break
                else:
                    FILE1dex = 0
                    self.FILE2.pop(0)
                    continue

            try: ## Load from file 2
                line2 = self.FILE2[0]
                l2start = line2[0]
                l2end   = line2[1]
            except IndexError:
                break

            if l1start > l2end:
                FILE1dex = 0
                self.FILE2.pop(0)
                continue

            if l2start > l1end:
                self.FILE1.pop(0)
                continue

            ## Once this point is reached, an overlap has been found!
            aligns = aligns + 1
            alignment_number = lines_up(l2start, l2end, l1start, l1end)
            self.output(line2[2], line1[2], alignment_number)
            FILE1dex += 1
        
        ## Close outputs
        del(self.FILE1)
        del(self.FILE2)
        self.writefile.close()
        log.close()
        print("Closed",self.writefile_name)

        return aligns

