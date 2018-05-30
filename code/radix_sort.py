#A program that implements radix sort in place
from math import log10
from random import randint
def xplace(n, x):
    "Returns digit in x place of x, 0 being ones place"
    return (n//(10**x))%10

def test_xplace(n):
    for i in range(1,n+1):
        print("TEST",i)
        print("==========")
        x = randint(0,10)
        y = randint(0,10**x)
        z = randint(0,len(str(y))-1)
        print("NUM:",y)
        print("PLC:"," "*(len(str(y))-z-1) + "^"+str(z))
        print("VAL:",xplace(y,z))
        print()
    return

def radix_sort(list_to_sort):
    """Given a list to sort, sorts the list in place via radix sort
    assumes that the list contains tuples. sorts by the first item
    in the tuple"""
    BUCKETS = []
    for i in range(10):
        BUCKETS.append([])
    lognum = 0
    for entry in list_to_sort:
        newlognum = int(log10(entry[0]))
        if newlognum > lognum:
            lognum = newlognum
    for DIGIT in range(lognum+1):
        for i in list_to_sort:
            current_digit = xplace(i[0],DIGIT)
            BUCKETS[current_digit].append(i)
        index = 0
        for bucket in BUCKETS:
            for item in bucket:
                list_to_sort[index] = item
                index += 1
        BUCKETS = []
        for i in range(10):
            BUCKETS.append([])
    return
"""
X = []
for x in range(500):
    X.append((randint(0,100000000),"H"*randint(0,10)))
radix_sort(X)
if X[0]:
    for x in X:
        print(x)

"""
