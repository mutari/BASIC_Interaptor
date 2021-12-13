import json
import sys
from BASICParser import Parser
from BASICInteraptor import Interaptor
from setManager import SetManager
from helpFunctions import getFileInput, createHashMap

commandList = []
commandMap = {}

# python3 main.py {bas file} {set name} {mode (dev|pro)} {var1 name} {värde1} {var2 name} {värde2}

if len(sys.argv) > 1:
    script = sys.argv[1]
else:
    script = "main.bas"

if len(sys.argv) > 2:
    manager_name = sys.argv[2]
else:
    manager_name = "main"

if len(sys.argv) > 3:
    mode = sys.argv[3]
else:
    mode = "pro"

commandList = getFileInput(script)

commandMap = createHashMap(commandList)
#print(commandMap)

parser = Parser(manager_name)
tokens = parser.ParseMap(commandMap)
#print(json.dumps(tokens, indent=2))
#print(parser.getCommandMap())

funktionManager = SetManager()

interaptor = Interaptor(funktionManager, manager_name, mode)

f = funktionManager.getByName(manager_name)

for i in range(4, len(sys.argv), 2):
    f.createNewVar(sys.argv[i], sys.argv[i+1])

interaptor.interapt(tokens)

#print(json.dumps(f.VarList, indent=2))
#print(json.dumps(f.ArrayList, indent=2))