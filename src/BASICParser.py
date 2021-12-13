import re

# >=, <=, >, <, ==

class Parser:

    def __init__(self, mode):
        self.CommandMap = {}

    def ParseMap(self, cm): 
        self.CommandMap = cm

        Tokens = {}

        for key in self.CommandMap:
            rowTokens = {}
            #print(": " + self.CommandMap[key])
            #print("- " + key)
            chars = self.split(self.CommandMap[key])
            cmd = ""
            index = 0
            
            string = ""
            IsString = 0

            number = ""
            IsNumber = 0

            it = iter(range(0, len(chars)))

            for c in it:
                cmd += chars[c]
                #print(cmd)
                
                #fi the parser have fin a string
                if IsString == 1:
                    if cmd != "\"": 
                        string += cmd
                        cmd = ""
                    else: # end of string
                        rowTokens[index] = self.addTokenObjekt("STR", string)
                        string = ""
                        cmd = ""
                        IsString = 0
                        index += 1
                #if the parser have find a number
                if IsNumber == 1:
                    if self.isNumber(cmd) == 1:
                        number += cmd
                        cmd = ""
                        if self.isNumber(chars[c+1]) == 0:
                            #print("test")
                            rowTokens[index] = self.addTokenObjekt("NUM", number)
                            number = ""
                            IsNumber = 0
                            index += 1
                    else:
                        return {"error": "could not work out a number row: " + key}

                elif cmd == " " or cmd == "\t" or cmd == "\n": # make the candy go away
                    cmd = ""
                elif cmd == "\"": # start of string 
                    IsString = 1
                    cmd = ""
                
                #start of a number
                elif self.isNumber(cmd) == 1:
                    number += cmd
                    IsNumber = 1
                    cmd = ""
                    if self.isNumber(chars[c+1]) == 0:
                            #print("test")
                            rowTokens[index] = self.addTokenObjekt("NUM", number)
                            number = ""
                            IsNumber = 0
                            index += 1
                
                #test of operations
                elif cmd == "=":
                    if chars[c+1] != "=":
                        rowTokens[index] = self.addTokenObjekt("OPERATOR", "EQ")
                    else:
                        rowTokens[index] = self.addTokenObjekt("BOOLEANSKOP", "EQEQ")
                        next(it)
                    cmd = ""
                    index += 1
                elif cmd == "<":
                    if chars[c+1] != "=":
                        rowTokens[index] = self.addTokenObjekt("BOOLEANSKOP", "LT")
                    else:
                        rowTokens[index] = self.addTokenObjekt("BOOLEANSKOP", "LTEQ")
                        next(it)
                    cmd = ""
                    index += 1
                elif cmd == ">":
                    if chars[c+1] != "=":
                        rowTokens[index] = self.addTokenObjekt("BOOLEANSKOP", "MT")
                    else:
                        rowTokens[index] = self.addTokenObjekt("BOOLEANSKOP", "MTEQ")
                        next(it)
                    cmd = ""
                    index += 1
                elif cmd == "!=":
                    rowTokens[index] = self.addTokenObjekt("BOOLEANSKOP", "NEQ")
                    cmd = ""
                    index += 1
                elif cmd == "+":
                    rowTokens[index] = self.addTokenObjekt("OPERATOR", "PLUS")
                    cmd = ""
                    index += 1
                elif cmd == "-":
                    rowTokens[index] = self.addTokenObjekt("OPERATOR", "MINUS")
                    cmd = ""
                    index += 1
                elif cmd == "*":
                    rowTokens[index] = self.addTokenObjekt("OPERATOR", "MULTIPLIKATION")
                    cmd = ""
                    index += 1
                elif cmd == ",":
                    rowTokens[index] = self.addTokenObjekt("OPERATOR", "COMMA")
                    cmd = ""
                    index += 1
                elif cmd == "[":
                    rowTokens[index] = self.addTokenObjekt("OPERATOR", "LEFTBLOCK")
                    cmd = ""
                    index += 1
                elif cmd == "]":
                    rowTokens[index] = self.addTokenObjekt("OPERATOR", "RIGHTBLOCK")
                    cmd = ""
                    index += 1
                elif cmd == ";":
                    rowTokens[index] = self.addTokenObjekt("OPERATOR", "APPOSTROF")
                    cmd = ""
                    index += 1

                #test for static tiped words
                elif cmd == "PRINT" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "PRINT")
                    cmd = ""
                    index += 1
                elif cmd == "LET" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "LET")
                    cmd = ""
                    index += 1
                elif cmd == "GOTO" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "GOTO")
                    cmd = ""
                    index += 1
                elif cmd == "ARRAY" and self.getNext(chars, c+1) == " ": 
                    rowTokens[index] = self.addTokenObjekt("STATIC", "ARRAY")
                    cmd = ""
                    index += 1
                elif cmd == "INPUT" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "INPUT")
                    cmd = ""
                    index += 1
                elif cmd == "END" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("STATIC", "END")
                    cmd = ""
                    index += 1
                elif cmd == "IF" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "IF")
                    cmd = ""
                    index += 1
                elif cmd == "THEN" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("STATIC", "THEN")
                    cmd = ""
                    index += 1
                elif cmd == "ELSE" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("STATIC", "ELSE")
                    cmd = ""
                    index += 1
                elif cmd == "FOR" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "FOR")
                    cmd = ""
                    index += 1
                elif cmd == "TO" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "TO")
                    cmd = ""
                    index += 1
                elif cmd == "STEP" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "STEP")
                    cmd = ""
                    index += 1
                elif cmd == "NEXT" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "NEXT")
                    cmd = ""
                    index += 1
                elif cmd == "GOSUB" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "GOSUB")
                    cmd = ""
                    index += 1
                elif cmd == "NAMESPACE" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "NAMESPACE")
                    cmd = ""
                    index += 1
                elif cmd == "IMPORT" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "IMPORT")
                    cmd = ""
                    index += 1
                elif cmd == "AS" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "AS")
                    cmd = ""
                    index += 1
                elif cmd == "RETURN" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("STATIC", "RETURN")
                    cmd = ""
                    index += 1
                elif cmd == "PLOT" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "PLOT")
                    cmd = ""
                    index += 1
                elif cmd == "DISPLAY" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "DISPLAY")
                    cmd = ""
                    index += 1
                elif cmd == "DRAW" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "DRAW")
                    cmd = ""
                    index += 1
                elif cmd == "TEXT" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "TEXT")
                    cmd = ""
                    index += 1
                elif cmd == "PAUSE" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("STATIC", "PAUSE")
                    cmd = ""
                    index += 1
                elif cmd == "EXPORT" and self.getNext(chars, c+1) == " ":
                    rowTokens[index] = self.addTokenObjekt("STATIC", "EXPORT")
                    cmd = ""
                    index += 1
                elif cmd == "CLS" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("STATIC", "CLS")
                    cmd = ""
                    index += 1
                elif cmd == "CLT" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("STATIC", "CLT")
                    cmd = ""
                    index += 1
                elif cmd == "CLC" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("STATIC", "CLC")
                    cmd = ""
                    index += 1
                elif cmd == "REM" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"): #if its a note then it just hops ower it
                    rowTokens[index] = self.addTokenObjekt("STATIC", "REM")
                    cmd = ""
                    break
                elif cmd == "FALSE" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("BOOLEAN", "FALSE")
                    cmd = ""
                    index += 1
                elif cmd == "TRUE" and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n"):
                    rowTokens[index] = self.addTokenObjekt("BOOLEAN", "TRUE")
                    cmd = ""
                    index += 1

                    
                    #check for var
                elif len(cmd) > 0 and (self.getNext(chars, c+1) == " " or self.getNext(chars, c+1) == "\n" or self.getNext(chars, c+1) == "," or self.getNext(chars, c+1) == "]"):
                    rowTokens[index] = self.addTokenObjekt("VAR", cmd)
                    cmd = ""
                    index += 1


                #check for variabels a variabel name can only be one char long
                #needs a loot of work
                elif len(cmd) > 0 and (self.getNext(chars, c+1) == "["):
                    rowTokens[index] = self.addTokenObjekt("VARARRAY", cmd)
                    cmd = ""
                    index += 1

                #   funktions i need
                #       COLOR()
                #       GETCHAR()
                #       GETCLICK()
                #       LEN()
                #       CHR()
                #       TIME()
                #       
                    

            Tokens[key] = rowTokens
        return Tokens

    def addTokenObjekt(self, t, v):
        tempToken = {}
        tempToken["type"] = t
        tempToken["value"] = v
        return tempToken 

    def split(self, word): 
        return [char for char in word]  


    def getCommandMap(self):
        return self.CommandMap 

    def getNext(self, chars, index):
        #print(len(chars), index)
        if len(chars) > index:
            #print("out: " + chars[index])
            return chars[index]
        return -1

    def isNumber(self, char):
        p = re.compile('[0-9]+')
        if p.match(char):
            return 1
        return 0 
    
    def isBokstav(self, char):
        p = re.compile('[a-zA-Z]+')
        if p.match(char): 
            return 1
        return 0

    def isOporation(self, char):
        p = re.compile('[-+*/=><()]+')
        if p.match(char):
            return 1
        return 0