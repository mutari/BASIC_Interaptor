import json
import sys
from BASICParser import Parser
from BASICInterrupter import Interrupter
from setManager import SetManager
from helpFunctions import get_file_input, create_hash_map

command_list = []
command_map = {}

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

if len(sys.argv) > 4:
    debug = sys.argv[4]
else:
    debug = "false"

command_list = get_file_input(script)

command_map = create_hash_map(command_list)
if debug == 'true':
    print(command_map)

parser = Parser(manager_name)
tokens = parser.parse_map(command_map)
#print(json.dumps(tokens))

if debug == 'true':
    print(json.dumps(tokens, indent=2))
    print(parser.get_command_map())

funktion_manager = SetManager()

interrupter = Interrupter(funktion_manager, manager_name, mode)

f = funktion_manager.get_by_name(manager_name)

for i in range(5, len(sys.argv), 2):
    f.create_new_var(sys.argv[i], sys.argv[i + 1])

interrupter.interrupt(tokens)

if debug == 'true':
    print(json.dumps(f.VarList, indent=2))
    print(json.dumps(f.ArrayList, indent=2))
