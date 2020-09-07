from parser import Parser
from interaptor import Interaptor
from setManager import SetManager
import json
import sys

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

commandList = getFileInput(script)

commandMap = createHashMap(commandList)
#print(commandMap)

parser = Parser()
tokens = parser.ParseMap(commandMap)
print(json.dumps(tokens, indent=2))
#print(parser.getCommandMap())

funktionManager = SetManager()

interaptor = Interaptor(funktionManager, "hello")

f = funktionManager.getByName("hello")
#print(f.getName())

interaptor.interapt(tokens)