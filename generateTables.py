import time
from lib import *
 
def nextPass():
    nextInitPass[0] += 1
    b62 = baseN(nextInitPass[0], 4)
    b62 = b62[::-1]
    return b62
 
def repeat(h4sh, lookup):
    for key in lookup.keys():
        if h4sh == key:
            return True
    return False
 
def genChain(chainLength, tableNo, init, lookup):
    hashed = md5(init)
    #print init, hashed
   
    for i in range(1, chainLength):
        pw = reduc(hashed, i, tableNo)
        hashed = md5(pw)
        #print pw, hashed

    return [init, hashed]
 
def genTable(tableLength, chainLength, tableNo, seed):
    lookup = {}
    start = int(time.time())
    f = open("tables/" + 'table' + str(tableNo) + '.txt', 'w')
    init = seed
   
    i = 0
    collisions = 0
    while(i < tableLength):
        chainOutput = genChain(chainLength, tableNo, init, lookup)
        if not repeat(chainOutput[1], lookup):
            lookup[chainOutput[1]] = chainOutput[0]
            f.write(chainOutput[0])
            f.write(' ')
            f.write(chainOutput[1])
            f.write(' ')
            if (i+1) % 5000 == 0:
                end = int(time.time())
                print "Chain %d completed. Elapsed: %d. Collisions: %d" % (int(i+1), int(end - start), collisions)
        else:
            #print "Chain %d failure" % i
            collisions += 1
            i -= 1
        init = nextPass()
        i += 1
    #print 'nextInitPass: ' + init
    f.close()
 
for i in range(1):
    print "Table " + str(i+1) + " generation in progress..."
    genTable(tableLength, chainLength, i+1, baseN(nextInitPass[0], totalTables-1))
    print "Table " + str(i+1) + " done.\n"