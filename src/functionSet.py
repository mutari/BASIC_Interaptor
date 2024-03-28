import time
from helpFunctions import get_file_input, create_hash_map


class FunctionSet:

    def __init__(self, threadname, mode):
        self.name = threadname
        self.VarList = []
        self.ArrayList = []
        self.OldIndexes = []
        self.forLoop = []
        self.namespace = ""
        self.mode = mode

    # basic static functions
    def PRINT(self, tokens):
        str = self.advancedEval(tokens)
        self.basicPrint(str)

    def LET(self, name, value):
        self.createNewVar(name["value"], self.advancedEval(value))

    def ARRAY_CREATE(self, name, dim):
        self.createNewArray(name["value"], dim)

    def ARRAY_UPPDATE(self, name, data):
        array = self.getArrayByName(name)
        key = self.generateArrayKeys(data)

        # test if the right amount of array keys
        if key["keysFound"] > int(array["dimension"]):
            print("to meny keys" + str(key) + " array: " + str(array))
            exit(1)
        elif key["keysFound"] < int(array["dimension"]):
            print("to fjue keys: " + str(key) + " array: " + str(array))
            exit(1)

        if data[list(data.items())[key["endOfKeys"]][0]]["value"] == "EQ":
            data = self.slice(data, key["endOfKeys"] + 1)
            value = self.advancedEval(data)
            self.uppdateArray(name, key["keys"], value)

    def INPUT(self, varName, text):
        text = self.advancedEval(text)
        value = self.basicInput(text)
        self.createNewVar(varName["value"], value)

    def GOTO(self, data):
        number = self.advancedEval(data)
        return number

    def GOSUB(self, data, oldIndex):
        number = self.advancedEval(data)
        self.OldIndexes.append(oldIndex)
        return number

    def RETURN(self):
        try:
            return self.OldIndexes.pop(len(self.OldIndexes) - 1)
        except:
            return None

    def PAUSE(self, data):
        t = self.advancedEval(data)
        time.sleep(t)

    def IF(self, case):
        opeIndex = list(case.items())[self.getKeyOf(case, "BOOLEANSKOP", "type")][0]
        operator = case[opeIndex]["value"]
        value1 = self.advancedEval(self.slice(case, 0, opeIndex - 1))
        value2 = self.advancedEval(self.slice(case, opeIndex))
        if operator == "EQEQ":
            operator = "=="
        elif operator == "LT":
            operator = "<"
        elif operator == "LTEQ":
            operator = "<="
        elif operator == "MT":
            operator = ">"
        elif operator == "MTEQ":
            operator = ">="
        elif operator == "NEQ":
            operator = "!="

        if not self.is_number(value1):
            value1 = "\"" + str(value1) + "\""
        else:
            value1 = str(value1)

        if not self.is_number(value2):
            value2 = "\"" + str(value2) + "\""
        else:
            value2 = str(value2)

        return eval(value1 + " " + str(operator) + " " + value2)

    def FOR(self, data, rowIndex):
        keyTO = self.getKeyOf(data, "TO")
        keySTEP = self.getKeyOf(data, "STEP")

        # create a variable
        var = self.slice(data, 0, keyTO)
        keys = list(data.items())
        varName = var[1]
        if (var[2]["value"] == "EQ"):
            self.LET(varName, self.slice(var, 2))
        else:
            print("Error interaptor: missing EQ when declearing var")
            exit(1)

        goal = None
        step = None
        if (keySTEP):
            goal = self.slice(data, keyTO, keySTEP)
            step = self.slice(data, keySTEP + 1)
            step = self.advancedEval(step)
        else:
            goal = self.slice(data, keyTO + 1)
            step = 1
        goal = self.advancedEval(goal)

        self.forLoop.append({"var": varName, "goal": goal, "step": step, "row": rowIndex})

    def NEXT(self, varName):
        loop = self.forLoop[len(self.forLoop) - 1]
        if loop["var"]["value"] != varName[1]["value"]:
            print("Forloops in wrong queue")
            exit(1)
        value = self.getVarByName(loop["var"]["value"])
        if int(value["value"]) + int(loop['step']) >= int(loop["goal"]):
            self.forLoop.pop(len(self.forLoop) - 1)
            self.uppdateVar(loop["var"]["value"], "None")  # borde ändra till att döda variablen
            return None
        self.uppdateVar(loop["var"]["value"], int(value["value"]) + int(loop["step"]))
        return loop["row"]

    def LOAD(self, data):
        name = list(data.items())[0][1]['value']
        if name == "NOW":
            self.createNewVar(name, int(time.time() * 1000000))
        elif name == "SEC":
            self.createNewVar(name, int(time.time()))

    def NAMESPACE(self, tokens):
        namespace = self.advancedEval(tokens)
        self.namespace = namespace

    def IMPORT(self, path, importVar):

        commandList = get_file_input(path)
        print(commandList)

        print(path, importVar)

    def EXPORT(self, data):
        var = self.getVarByName(data[1]["value"])
        print("exp:" + str(var["name"]) + ":" + str(var["value"]))

    # var functions
    def getVarByName(self, name):
        name = self.getNamespace(name);
        for var in self.VarList:
            if var["name"] == name:
                return var
        print("Error: array whit name: " + str(name) + " is not deklarerad ")
        exit(1)

    def createNewVar(self, name, value):
        name = self.getNamespace(name);
        for var in self.VarList:
            if var["name"] == name:
                var["value"] = value  # if var exists overide it
                return
        self.VarList.append({"name": name, "value": value})
        # print(self.VarList)

    def uppdateVar(self, name, value):
        name = self.getNamespace(name);
        var = self.getVarByName(name)
        var["value"] = value

    # array functions
    def getArrayByName(self, name):
        name = self.getNamespace(name);
        for array in self.ArrayList:
            if array["name"] == name:
                return array
        print("Error: array whit name: " + str(name) + " is not deklarerad ")
        exit(1)

    def createNewArray(self, name, dim):
        name = self.getNamespace(name);
        self.ArrayList.append({"name": name, "dimension": dim, "value_list": {}})

    def uppdateArray(self, name, keys, value):
        array = self.getArrayByName(name)
        array["value_list"][keys] = value

    def getNamespace(self, name):
        if len(name.split('@')) > 1:
            return name
        if self.namespace != "":
            name = self.namespace + "@" + name
        return name

    def generateArrayKeys(self, data):
        keys = ""
        # get the arraý keys
        endOfKeys = -1
        keysfound = 0
        exp = False
        expObj = {}
        it = iter(range(list(data.items())[0][0], len(data) + list(data.items())[0][0]))
        for c in it:
            if data[c]["value"] == "LEFTBLOCK":
                exp = True
                continue
            elif data[c]["value"] == "RIGHTBLOCK":
                keysfound += 1
                if keys != "":
                    keys += ',' + str(self.advancedEval(expObj))
                else:
                    keys += str(self.advancedEval(expObj))
                expObj = {}
                exp = False
                if c + 1 >= len(data) + list(data.items())[0][0]:
                    endOfKeys = c - (int(list(data.items())[0][0]) - 1)
                    break
                elif data[c + 1]["value"] != "LEFTBLOCK":
                    endOfKeys = c - (int(list(data.items())[0][0]) - 1)
                    break
                else:
                    continue
                    # rewrite to suport advancedEval
            elif exp:
                expObj[c] = data[c]
            else:
                print("Array syntax error data :: " + str(data))
                exit
        return {"endOfKeys": endOfKeys, "keysFound": keysfound, "keys": keys}

    # bas functions
    def getName(self):
        return self.name

    # omvandlar variablar till des värde
    def translate(self, input):
        out = {}
        it = iter(range(0, len(input)))
        for c in it:
            # list(input.items())[0][0] gets the first key of the dic
            token = input[c + list(input.items())[0][0]]
            if token["type"] == "VAR":
                value = self.getVarByName(token["value"])["value"]
                if self.is_number(value):
                    out[c] = ({"type": "NUM", "value": value})
                else:
                    out[c] = ({"type": "STR", "value": value})
            elif token["type"] == "VAR_ARRAY":
                key = self.generateArrayKeys(self.slice(input, c + 1))
                for j in range(0, key["endOfKeys"]):
                    next(it)
                value = self.getArrayByName(token["value"])["value_list"][key["keys"]]
                if self.is_number(value):
                    out[c] = ({"type": "NUM", "value": value})
                else:
                    out[c] = ({"type": "STR", "value": value})
            else:
                out[c] = (token)
        return out

    # evulerar utan sträng
    def evalNum(self, input):
        out = ""
        for c in input:
            value = input[c]["value"]
            key = input[c]["type"]
            # print(self.VarList)
            if key == "NUM":
                out += str(value)
            elif key == "OPERATOR":
                if value == "PLUS":
                    out += "+"
                elif value == "MINUS":
                    out += "-"
                elif value == "MULTIPLIKATION":
                    out += "*"
                elif value == "SLASH":
                    out += "/"
                elif value == "LEFTPARENTHESIS":
                    out += "("
                elif value == "RIGHTPARENTHESIS":
                    out += ")"
            else:
                return False

        return eval(out)

    # evulerar med sträng
    def evalStr(self, input):
        out = ""
        # change all loops to while loops

        i = 0
        while i < len(input):
            token = input[list(input.items())[i][0]]
            if i % 2 == 0:  # if first item
                if token["type"] == "STR":
                    out += str(token["value"])
                elif token["type"] == "NUM":
                    out += str(token["value"])
                else:
                    return "Error evalStr input :: " + str(input)
                    exit
            elif token["value"] != "PLUS" and token["value"] != "MINUS":
                return "Error evalStr input :: " + str(input)
                exit
            i += 1

        return out

    def is_number(self, char):
        return str(char).isdecimal()

    def basicPrint(self, value):
        print(value)

    def basicInput(self, text):
        return input(text)

    def advancedEval(self, value):
        # translates all the variabels to ther value
        trans = self.translate(value)

        # returns False if the value have a char that is not a number
        res = self.evalNum(trans)
        if res is False:
            # if value is not a string
            res = self.evalStr(trans)
        return res

    def slice(self, dic, start, end=None):
        return dict(list(dic.items())[start:end])

    def getKeyOf(self, data, val, index="value"):
        i = 0
        while i < len(data):
            if data[list(data.items())[i][0]][index] == val:
                return i
            i += 1
        return None
