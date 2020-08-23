from functionSet import FunctionSet
import itertools

# I Think Working
# PRINT
# LET
# ARRAY
# INPUT
# END
# GOTO
# GOSUB ... RETURN
# PAUSE
# IF ... THEN
# IF ... THEN ... ELSE

# To Do

# Statements
# FOR ... TO ... STEP ... NEXT

# Graphics
# PLOT
# DISPLAY
# DRAW
# TEXT

# Clear
# CLS
# CLC

# funtcions
# RND()
# CHR()
# LEN()
# COLOR()
# GETCHAR()
# GETCLICK()

class Interaptor:

    STATIC = "STATIC"
    VARARRAY = "VARARRAY"
    VAR = "VAR"


    def __init__(self, setManager, functionSetName, new = True):
        self.rowIndex = 0
        if new:
            self.functions = FunctionSet(functionSetName)
            self.manager = setManager
            self.manager.addSet(self.functions)
        else:
            self.manager = setManager
            self.functions = self.manager.getByName(functionSetName)

    def moveCodeIndex(self, tokens, index = 0): 
        temp = list(tokens.keys())[index]
        self.rowIndex = index + 1
        return temp

    def interapt(self, tokens):
        
        codeIndex = self.moveCodeIndex(tokens, self.rowIndex)

        while(True):
            #print(tokens)
            #print("test: " + str(self.rowIndex))
            #print(codeIndex)

            #code index is the row number
            #it = iter(range(0, len(tokens[codeIndex])))
            #for c in it:
            # c is the index of the pecefic token in the row 
            c = list(tokens[codeIndex].items())[0][0]
            Checking = tokens[codeIndex][c]

            if Checking["type"] == Interaptor.STATIC:
                #check is the command starts white a static key name
                if Checking["value"] == "REM":
                    if(self.rowIndex < len(tokens)):
                        codeIndex = self.moveCodeIndex(tokens, self.rowIndex)
                    else: 
                        break
                    continue
                if Checking["value"] == "PRINT":
                    #print("PRINT:::: " + str(tokens[codeIndex]))
                    self.functions.PRINT(self.slice(tokens[codeIndex], 1))
                elif Checking["value"] == "LET":
                    #print("LET:::: " + str(tokens[codeIndex]))
                    varName = tokens[codeIndex][c+1]
                    if(tokens[codeIndex][c+2]["value"] == "EQ"):
                        #print(self.slice(tokens[codeIndex], 3))
                        self.functions.LET(varName, self.slice(tokens[codeIndex], 3))
                    else:
                        print("Error interaptor122")
                        exit
                elif Checking["value"] == "ARRAY":
                    arrayName = tokens[codeIndex][c+1]
                    arrayDim = 1
                    #print("Array name: " + str(arrayName["value"])) 
                    if c+2 < len(tokens[codeIndex]) and tokens[codeIndex][c+2]["value"] == "COMMA":
                        arrayDim = tokens[codeIndex][c+3]["value"]
                    self.functions.ARRAY_CREATE(arrayName, arrayDim)
                elif Checking["value"] == "INPUT":
                    data = self.slice(tokens[codeIndex], 1)
                    index = self.getIndexOf(data, "APPOSTROF")
                    text = self.slice(data, 0, index)
                    varName = data[list(self.slice(data, index+1).items())[0][0]]
                    self.functions.INPUT(varName, text)
                elif Checking["value"] == "END":
                    print("The Script Whs Terminated(row: " + codeIndex + ")")
                    exit
                elif Checking["value"] == "GOTO":
                    number = self.functions.GOTO(self.slice(tokens[codeIndex], 1))
                    codeIndex = self.moveCodeIndex(tokens, self.findRowIndexByKey(tokens, number))
                    continue
                elif Checking["value"] == "GOSUB":
                    number = self.functions.GOSUB(self.slice(tokens[codeIndex], 1), codeIndex)
                    codeIndex = self.moveCodeIndex(tokens, self.findRowIndexByKey(tokens, number))
                    continue
                elif Checking["value"] == "RETURN":
                    number = self.functions.RETURN()
                    if number != None:
                        codeIndex = self.moveCodeIndex(tokens, self.findRowIndexByKey(tokens, number))
                        codeIndex = self.moveCodeIndex(tokens, self.rowIndex)
                        continue
                elif Checking["value"] == "PAUSE":
                    self.functions.PAUSE(self.slice(tokens[codeIndex], 1))
                elif Checking["value"] == "IF":
                    statement = self.slice(tokens[codeIndex], 1, self.getIndexOf(tokens[codeIndex], "THEN"))
                    code = self.slice(tokens[codeIndex], self.getIndexOf(tokens[codeIndex], "THEN")+1, self.getIndexOf(tokens[codeIndex], "ELSE"))
                    #print(code)
                    if self.functions.IF(statement):
                        row = {}
                        #print("tokens: " + str(tokens[codeIndex]))
                        rowKey = list(tokens.keys())[self.rowIndex-1]
                        row[rowKey] = code
                        #create a new interaptor white the same functionset
                        Interaptor(self.manager, "hello", False).interapt(row)
                    elif self.getIndexOf(tokens[codeIndex], "ELSE") != None:
                        alternativCode = self.slice(tokens[codeIndex], self.getIndexOf(tokens[codeIndex], "ELSE")+1)
                        row = {}
                        #print("tokens: " + str(tokens[codeIndex]))
                        rowKey = list(tokens.keys())[self.rowIndex-1]
                        row[rowKey] = alternativCode
                        #create a new interaptor white the same functionset
                        Interaptor(self.manager, "hello", False).interapt(row)
                else:
                    print("Error interaptor 123")
                    exit
            elif Checking["type"] == Interaptor.VARARRAY:
                arrayName = Checking["value"]
                keys = self.slice(tokens[codeIndex], 1)
                #print("keys: " + str(keys))
                self.functions.ARRAY_UPPDATE(arrayName, keys)
            #print(tokens[codeIndex][c]["value"])

            #move tokens list forward
            if(self.rowIndex < len(tokens)):
                codeIndex = self.moveCodeIndex(tokens, self.rowIndex)
            else: 
                break

    
    def slice(self, dic, start, end = None):
        return dict(list(dic.items())[start:end])

    def getIndexOf(self, data, val, index = "value"):
        i = 0
        while i < len(data):
            if data[list(data.items())[i][0]][index] == val:
                return i
            i += 1
        return None

    def findRowIndexByKey(self, tokens, key):
        tokens = list(tokens.keys())
        i = 0
        while i < len(tokens):
            if tokens[i] == str(key):
                return i
            i += 1
        return None



