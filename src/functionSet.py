import re
import time

class FunctionSet:
    
    def __init__(self, threadname):
        self.name = threadname
        self.VarList = []
        self.ArrayList = []
        self.OldIndexes = []
        self.forLoop = []

    #basic static functions
    def PRINT(self, tokens):
        str = self.advancedEval(tokens)
        self.basicPrint(str)
        #print(self.VarList)

    def LET(self, name, value):
        #print(self.translate(value))
        self.createNewVar(name["value"], self.advancedEval(value))
        #print("varList: " + str(self.VarList))

    def ARRAY_CREATE(self, name, dim):
        #print("array name: " + str(name) + "     dimension: " + str(dim))
        self.createNewArray(name["value"], dim)
        #print("arrayList: " + str(self.ArrayList))

    def ARRAY_UPPDATE(self, name, data):
        array = self.getArrayByName(name)

        key = self.generateArrayKeys(data)

        #print("key: " + str(key) + ",  " + str(array["dimension"]))

        #test if the right amount of array keys
        if key["keysFound"] > int(array["dimension"]):
            print("to meny keys")
            exit(1)
        elif key["keysFound"] < int(array["dimension"]):
            print("to fjue keys: " + str(key) + " array: " + str(array))
            exit(1)
        #else:
        #   print("perfekt")

        #print("keys: " + str(key))

        #print("data: " + str(data))
        #print("endOfKey: " + str(key["endOfKeys"]))

        if data[list(data.items())[key["endOfKeys"]][0]]["value"] == "EQ":
            data = self.slice(data, key["endOfKeys"]+1)
            #print(data)
            value = self.advancedEval(data)
            self.uppdateArray(name, key["keys"], value)
            #print("Array: " + str(self.ArrayList))

    def INPUT(self, varName, text):
        #print("var: " + str(varName) + "    text: " + str(text))
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
            return self.OldIndexes.pop(len(self.OldIndexes)-1)
        except:
            return None

    def PAUSE(self, data):
        t = self.advancedEval(data)
        time.sleep(t)

    def IF(self, case):
        opeIndex = list(case.items())[self.getKeyOf(case, "BOOLEANSKOP", "type")][0]
        operator = case[opeIndex]["value"]
        value1 = self.advancedEval(self.slice(case, 0, opeIndex-1))
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

        return eval("\"" + str(value1) + "\" " + str(operator) + " \"" + str(value2) + "\"")

    def FOR(self, data, rowIndex):
        keyTO = self.getKeyOf(data, "TO")
        keySTEP = self.getKeyOf(data, "STEP")

        # create a variable
        var = self.slice(data, 0, keyTO)
        keys = list(data.items())
        varName = var[1]
        if(var[2]["value"] == "EQ"):
            self.LET(varName, self.slice(var, 2))
        else:
            print("Error interaptor: missing EQ when declearing var")
            exit(1)

        goal = None
        step = None
        if(keySTEP):
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
        if value["value"] + loop["step"] >= loop["goal"]:
            self.forLoop.pop(len(self.forLoop) - 1)
            self.uppdateVar(loop["var"]["value"], "None") # borde ändra till att döda variablen
            return None
        self.uppdateVar(loop["var"]["value"], value["value"] + loop["step"])
        return loop["row"]
        

    #var functions
    def getVarByName(self, name):
        for var in self.VarList:
            if var["name"] == name :
                return var
        print("Error: array whit name: " + str(name) + " is not deklarerad ")
        exit(1)

    def createNewVar(self, name, value):
        self.VarList.append({"name": name, "value": value})

    def uppdateVar(self, name, value):
        var = self.getVarByName(name)
        var["value"] = value

    #array functions
    def getArrayByName(self, name):
        for array in self.ArrayList:
            if array["name"] == name:
                return array
        print("Error: array whit name: " + str(name) + " is not deklarerad ")
        exit(1)

    def createNewArray(self, name, dim):
        self.ArrayList.append({"name": name, "dimension": dim, "value_list": {}})

    def uppdateArray(self, name, keys, value):
        array = self.getArrayByName(name)
        array["value_list"][keys] = value
    
    def generateArrayKeys(self, data):
        keys = ""
        #get the arraý keys
        endOfKeys = -1
        keysfound = 0
        it = iter(range(list(data.items())[0][0], len(data) + list(data.items())[0][0]))
        for c in it:
            #print(data[c])
            if data[c]["value"] == "LEFTBLOCK":
                continue
            elif data[c]["value"] == "RIGHTBLOCK":
                if c+1 >= len(data) + list(data.items())[0][0]:
                    endOfKeys = c - (int(list(data.items())[0][0])-1)
                    break
                elif data[c+1]["value"] != "LEFTBLOCK":
                    endOfKeys = c - (int(list(data.items())[0][0])-1)
                    break
                else:
                    continue 
            # test for vars to 
            elif data[c]["type"] == "NUM":
                keysfound += 1
                if keys != "":
                    keys += "," + str(data[c]["value"])
                else:
                    keys += str(data[c]["value"])
            else:
                print("Array syntax error data :: " + str(data))
                exit
        return {"endOfKeys": endOfKeys, "keysFound": keysfound, "keys": keys}


    #bas functions
    def getName(self):
        return self.name
    
    #omvandlar variablar till des värde
    def translate(self, input):
        #print("input:::" + str(input))
        out = {}
        it = iter(range(0, len(input)))
        for c in it:
            #list(input.items())[0][0] gets the first key of the dic
            token = input[c + list(input.items())[0][0]]
            if token["type"] == "VAR":
                value = self.getVarByName(token["value"])["value"]
                if self.isNumber(value):
                    out[c] = ({"type": "NUM", "value": value})
                else:
                    out[c] = ({"type": "STR", "value": value})
            elif token["type"] == "VARARRAY":
                #print("clisc :: " + str(self.slice(input, c + 1)))
                key = self.generateArrayKeys(self.slice(input, c + 1))
                #print("test:::: " + str(key))
                for j in range(0, key["endOfKeys"]):
                    next(it)
                #print(self.ArrayList)
                value = self.getArrayByName(token["value"])["value_list"][key["keys"]]
                if self.isNumber(value):
                    out[c] = ({"type": "NUM", "value": value})
                else:
                    out[c] = ({"type": "STR", "value": value})
                #print("key: " + str(key))
            else:
                out[c] = (token)
        return out

    #evulerar utan sträng
    def evalNum(self, input):
        out = ""
        #print("input: " + str(input))
        for c in input:
            #print("C: " + str(input[c]))
            value = input[c]["value"]
            key = input[c]["type"]
            if key == "NUM":
                out += str(value)
            elif key == "OPERATOR":
                if value == "PLUS":
                    out += "+"
                elif value == "MINUS":
                    out += "-"
                elif value == "MULTIPLIKATION":
                    out += "*"
            else:
                return False

        return eval(out)

    #evulerar med sträng
    def evalStr(self, input):
        out = ""
        #change all loops to while loops
        
        i = 0
        while i < len(input):
            token = input[list(input.items())[i][0]]
            #print("token: " + str(token))
            if i % 2 == 0 : #if first item
                if token["type"] == "STR":
                    out += str(token["value"])
                elif token["type"] == "NUM":
                    out += str(token["value"])
                else:
                    return "Error evalStr input :: " + str(input)
                    exit
            elif token["value"] != "PLUS":
                return "Error evalStr input :: " + str(input)
                exit
            i += 1

        return out

    def isNumber(self, char):
        return str(char).isdecimal()

    def basicPrint(self, value): 
        print(value)

    def basicInput(self, text):
        return input(text)

    def advancedEval(self, value):
        #print(value)
        #translates all the variabels to ther value
        trans = self.translate(value)
        
        #print("trans :: " + str(trans))
        #returns False if the value have a char that is not a number
        res = self.evalNum(trans)
        if res == False:
            #if value is not a string
            res = self.evalStr(trans)
        return res

    def slice(self, dic, start, end = None):
        return dict(list(dic.items())[start:end])

    def getKeyOf(self, data, val, index = "value"):
        i = 0
        while i < len(data):
            if data[list(data.items())[i][0]][index] == val:
                return i
            i += 1
        return None