import hashlib
import time
 
totalTables = 5
 
tableLength = 35220
chainLength = 500
passwordLength = 4
 
hashLength = 32
 
nextInitPass = [0]
modulus = 0
for i in range(1, 1 + passwordLength):
    modulus += 62 ** i
 
alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
 
def base62(decimalR, n):
    digit = ''
    dec = decimalR
    rem = dec % 62
    if n > 0:
        dec = (dec - rem) / 62
        digit += alphabet[rem] + base62(dec, n - 1)
        return digit
    else:
        return digit
   
def md5(password):
    return hashlib.md5(password).hexdigest()
       
def reduc(h4sh, columnNo, tableNo):
    dec = (int(h4sh, 16) + int(tableNo) + columnNo) % modulus
    b62 = ''
    for i in range(passwordLength, 0, -1):
        if(dec < 62 ** i):
            b62 = base62(dec, i)
            break;
        else:
            dec = dec - 62 ** i
    b62 = b62[::-1]
    return b62
 
def nextPass():
    nextInitPass[0] += 1
    b62 = base62(nextInitPass[0], 4)
    b62 = b62[::-1]
    return b62
 
def repeat(h4sh, lookup):
    for key in lookup.keys():
        if h4sh == key:
            return True
    return False
 
def genChain(chainLength, tableNo, init, lookup):
    ans = []
    hashed = md5(init)
    #print init, hashed
   
    for i in range(1, chainLength):
        pw = reduc(hashed, i, tableNo)
        hashed = md5(pw)
        #print pw, hashed
    lookup[hashed] = init
   
    return ans
 
def genTable(tableLength, chainLength, tableNo, seed, lookup):
    start = int(time.time())
    f = open('table' + str(tableNo) + '.txt', 'w')
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
    print 'nextInitPass: ' + init
    f.close()
 
def checkEndHash(h4sh, lookup):
    i = 0
    for key in lookup.keys():
        if h4sh == key:
            return i
        i += 1
    return -1
 
def crackHelper(h4sh, tableNo, lookup):
    line = []
    reductions = []
    for i in range(chainLength):
        x = h4sh
        for j in range(i, 0, -1):
            x = md5(reduc(x, chainLength - j, tableNo))
        endHashInd = checkEndHash(x, lookup)
        if(endHashInd != -1):
            line.append(endHashInd)
            reductions.append(i)
    return [line, reductions]
 
def crackTable(h4sh, filename, lookup):
    f = open(filename, 'r')
    for i in range(tableLength):
        password = f.read(passwordLength)
        f.seek(1,1)
        hashs = f.read(hashLength)
        f.seek(1,1)
        lookup[hashs] = password
 
    #check middle hashes
    iterationEndpoints = crackHelper(h4sh, filename[-5], lookup)
    if len(iterationEndpoints[0]) != 0:
        answer = []
        for index in range(len(iterationEndpoints[0])):
            #print lookup.values()[9215]
            #for i in range(1, 499):
                #answer[index] = reduc(md5(answer[index]), i, filename[-5])
            answer.append(lookup.values()[iterationEndpoints[0][index]])
            for i in range(1, chainLength - iterationEndpoints[1][index]):
                answer[index] = reduc(md5(answer[index]), i, filename[-5])
            if(md5(answer[index]) == h4sh):
                return answer[index]
    return "-1"
 
def crack(password):
    tableNum = 1
    print "Searching for hash of " + password
    while(tableNum <= totalTables):
        lookup = {}
        passw = crackTable(md5(password), 'table' + str(tableNum) + '.txt', lookup)
        if passw != "-1":
            return "Table " + str(tableNum) + "\nCRACKED! PASSWORD: " + passw
        tableNum += 1
    return "Password not found."
 
'''MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN'''
 
'''
genTable(tableLength, chainLength, 1, base62(nextInitPass[0], 4))
passwords = []
hashes = []
genTable(tableLength, chainLength, 2, base62(nextInitPass[0], 4))
passwords = []
hashes = []
genTable(tableLength, chainLength, 3, base62(nextInitPass[0], 4))
passwords = []
hashes = []
genTable(tableLength, chainLength, 4, base62(nextInitPass[0], 4))
passwords = []
hashes = []
genTable(tableLength, chainLength, 5, base62(nextInitPass[0], 4))
'''
 
'''
f = open("table1.txt", 'r')
for i in range(tableLength):
    password = f.read(passwordLength)
    f.seek(1,1)
    hashs = f.read(hashLength)
    f.seek(1,1)
    lookup[hashs] = password
'''
 
 
passwords = ['ankh', 'Baal', 'C0ke', 'D1sk', 'eASy', 'Flux', 'Gaga', 'Helm', 'Id0l', 'Java', 'Knob', 'L1es', 'M1d1',
            'N3rd', 'Omen', 'Paws', 'quid', 'ROFL', 'sync', 'TAC0', 'undo', 'VULN', 'whir', 'XraY', 'yuck', 'zer0',
            '45', 'pog', '666', 'g', 'l4Kk', 'v9F', 'Lwrf', 'Hi', 'Po47', 'llll', 'cAts', 'C94k', 'O9g', 'LK', 't4']
 
for passw in passwords:
    print crack(passw)
    print