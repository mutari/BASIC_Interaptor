import json
import sys
from parser import Parser
from interaptor import Interaptor
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
#print(f.getName())

interaptor.interapt(tokens)