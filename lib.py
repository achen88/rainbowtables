import hashlib

def baseN(decimalR, n):
    digit = ''
    dec = decimalR
    rem = dec % characterSpace
    if n > 0:
        dec = (dec - rem) / characterSpace
        digit += alphabet[rem] + baseN(dec, n - 1)
        return digit
    else:
        return digit

def md5(password):
    return hashlib.md5(password).hexdigest()
       
def reduc(h4sh, columnNo, tableNo):
    dec = (int(h4sh, 16) + int(tableNo) + columnNo) % modulus
    b62 = ''
    for i in range(passwordLength, 0, -1):
        if(dec < characterSpace ** i):
            b62 = baseN(dec, i)
            break;
        else:
            dec = dec - characterSpace ** i
    b62 = b62[::-1]
    return b62

config = open('config.txt', 'r')
totalTables = int(config.readline().split()[1])
tableLength = int(config.readline().split()[1])
chainLength = int(config.readline().split()[1])
passwordLength = int(config.readline().split()[1])
hashLength = int(config.readline().split()[1])
alphabet = config.readline().split()[1]

characterSpace = len(alphabet)
nextInitPass = [0]

modulus = 0
for i in range(1, 1 + passwordLength):
    modulus += characterSpace ** i