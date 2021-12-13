


def getFileInput(name):
    cmList = []
    f = open(name, "r")
    for x in f:
        cmList.append(x + " ")
    return cmList

def createHashMap(cmList):
    cmMap = {}
    for x in cmList:
        split = x.split(" ")
        number = split[0]
        del split[0]        
        if not number.isdecimal():
            continue
        cmMap[number] = " ".join(split)
    return cmMap