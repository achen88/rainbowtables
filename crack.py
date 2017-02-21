import sys
from lib import *

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
    f = open("tables/" + filename, 'r')
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
 
def crack(password, hashed):
    tableNum = 1
    
    while(tableNum <= totalTables):
        lookup = {}
        if not hashed:
            print "Searching for hash of " + password + " in table " + str(tableNum)
            passw = crackTable(md5(password), 'table' + str(tableNum) + '.txt', lookup)
        else:
            print "Looking for password with that hash in table " + str(tableNum)
            passw = crackTable(password, 'table' + str(tableNum) + '.txt', lookup)
        if passw != "-1":
            return "CRACKED! PASSWORD: " + passw
        tableNum += 1
    return "Password not found."

def usage():
    print "Flags:"
    print "    -test"
    print "    -password password_to_be_cracked"
    print "    -hash md5_hash_of_password_to_be_cracked"

if len(sys.argv) == 2:
    if sys.argv[1] == "-test":
        passwords = ['ankh', 'Baal', 'C0ke', 'D1sk', 'eASy', 'Flux', 'Gaga', 'Helm', 'Id0l', 'Java', 'Knob', 'L1es', 'M1d1',
            'N3rd', 'Omen', 'Paws', 'quid', 'ROFL', 'sync', 'TAC0', 'undo', 'VULN', 'whir', 'XraY', 'yuck', 'zer0',
            '45', 'pog', '666', 'g', 'l4Kk', 'v9F', 'Lwrf', 'Hi', 'Po47', 'llll', 'cAts', 'C94k', 'O9g', 'LK', 't4']
        for passw in passwords:
            print crack(passw, False)
            print ""
    else:
        usage()
elif len(sys.argv) == 3:
    if sys.argv[1] == "-password":
        print crack(sys.argv[2], False)
    elif sys.argv[1] == "-hash":
        print crack(sys.argv[2], True)
    else:
        usage()

else:
    usage()
    