import json
import sys
from BASICParser import Parser
from BASICInteraptor import Interaptor
from setManager import SetManager

commandList = []
commandMap = {}

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

# python3 main.py {bas file} {set name} {var1 name} {värde1} {var2 name} {värde2}

if len(sys.argv) > 1:
    script = sys.argv[1]
else:
    script = "main.bas"

if len(sys.argv) > 2:
    manager_name = sys.argv[2]
else:
    manager_name = "hello"

commandList = getFileInput(script)

commandMap = createHashMap(commandList)
#print(commandMap)

parser = Parser()
tokens = parser.ParseMap(commandMap)
#print(json.dumps(tokens, indent=2))
#print(parser.getCommandMap())

funktionManager = SetManager()

interaptor = Interaptor(funktionManager, manager_name)

f = funktionManager.getByName(manager_name)

for i in range(3, len(sys.argv), 2):
    f.createNewVar(sys.argv[i], sys.argv[i+1])

interaptor.interapt(tokens)