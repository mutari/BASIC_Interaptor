def get_token_object(t, v):
    return {"type": t, "value": v}


def split(word):
    return [char for char in word]


def get_next(chars, index):
    if len(chars) > index:
        return chars[index]
    return -1


class Parser:
    INVISIBLE_CHAR_LIST = [" ", "\t", "\n"]

    KEYWORDS_LIST = ["PRINT", "LET", "GOTO", "ARRAY", "INPUT", "END", "IF", "THEN", "ELSE", "FOR", "TO",
                     "STEP", "NEXT", "GOSUB", "NAMESPACE", "LOAD", "IMPORT", "AS", "RETURN", "PLOT",
                     "DISPLAY", "DRAW", "TEXT", "PAUSE", "EXPORT", "CLS", "CLT", "CLC", "REM", "FALSE", "TRUE"]

    OPERATORS_DICT = {
        '=': "OPERATOR", '<': "BOOLEANSKOP", '>': "BOOLEANSKOP", '!=': "BOOLEANSKOP", '+': "OPERATOR",
        '-': "OPERATOR", '*': "OPERATOR", '/': "OPERATOR", ',': "OPERATOR", '(': "OPERATOR", ')': "OPERATOR",
        '[': "OPERATOR", ']': "OPERATOR", ';': "OPERATOR"}

    def __init__(self, mode):
        self.CommandMap = {}

    def parse_map(self, cm):
        self.CommandMap = cm

        tokens = {}

        for key in self.CommandMap:
            row_tokens = {}
            # print(": " + self.CommandMap[key])
            # print("- " + key)
            chars = split(self.CommandMap[key])
            cmd = ""
            index = 0

            string = ""
            is_string = False

            number = ""
            is_number = False

            it = iter(range(0, len(chars)))

            for c in it:
                cmd += chars[c]
                # print(cmd)

                # if the parser have found a string
                if is_string:
                    if cmd != "\"":
                        string += cmd
                        cmd = ""
                    else:  # end of string
                        row_tokens[index] = get_token_object("STR", string)
                        string = ""
                        cmd = ""
                        is_string = False
                        index += 1

                # if the parser have found a number
                if is_number:
                    if cmd.isdigit():
                        number += cmd
                        cmd = ""
                        if not chars[c + 1].isdigit():
                            row_tokens[index] = get_token_object("NUM", number)
                            number = ""
                            is_number = False
                            index += 1
                    else:
                        return {"error": f"""could not work out a number row: {key}"""}

                elif cmd in self.INVISIBLE_CHAR_LIST:  # make the candy go away
                    cmd = ""
                elif cmd == "\"":  # start of string 
                    is_string = True
                    cmd = ""

                # start of a number
                elif cmd.isdigit():
                    number += cmd
                    is_number = True
                    cmd = ""
                    if not chars[c + 1].isdigit():
                        # print("test")
                        row_tokens[index] = get_token_object("NUM", number)
                        number = ""
                        is_number = False
                        index += 1

                # test of operations
                elif cmd == "=":
                    if chars[c + 1] != "=":
                        row_tokens[index] = get_token_object("OPERATOR", "EQ")
                    else:
                        row_tokens[index] = get_token_object("BOOLEANSKOP", "EQEQ")
                        next(it)
                    index += 1
                    cmd = ""
                elif cmd == "<":
                    if chars[c + 1] != "=":
                        row_tokens[index] = get_token_object("BOOLEANSKOP", "LT")
                    else:
                        row_tokens[index] = get_token_object("BOOLEANSKOP", "LTEQ")
                        next(it)
                    index += 1
                    cmd = ""
                elif cmd == ">":
                    if chars[c + 1] != "=":
                        row_tokens[index] = get_token_object("BOOLEANSKOP", "MT")
                    else:
                        row_tokens[index] = get_token_object("BOOLEANSKOP", "MTEQ")
                        next(it)
                    index += 1
                    cmd = ""
                elif cmd == "!=":
                    row_tokens[index] = get_token_object("BOOLEANSKOP", "NEQ")
                    index += 1
                    cmd = ""
                elif cmd == "+":
                    row_tokens[index] = get_token_object("OPERATOR", "PLUS")
                    index += 1
                    cmd = ""
                elif cmd == "-":
                    row_tokens[index] = get_token_object("OPERATOR", "MINUS")
                    index += 1
                    cmd = ""
                elif cmd == "*":
                    row_tokens[index] = get_token_object("OPERATOR", "MULTIPLIKATION")
                    index += 1
                    cmd = ""
                elif cmd == "/":
                    row_tokens[index] = get_token_object("OPERATOR", "SLASH")
                    index += 1
                    cmd = ""
                elif cmd == ",":
                    row_tokens[index] = get_token_object("OPERATOR", "COMMA")
                    index += 1
                    cmd = ""
                elif cmd == "(":
                    row_tokens[index] = get_token_object("OPERATOR", "LEFTPARENTHESIS")
                    index += 1
                    cmd = ""
                elif cmd == ")":
                    row_tokens[index] = get_token_object("OPERATOR", "RIGHTPARENTHESIS")
                    index += 1
                    cmd = ""
                elif cmd == "[":
                    row_tokens[index] = get_token_object("OPERATOR", "LEFTBLOCK")
                    index += 1
                    cmd = ""
                elif cmd == "]":
                    row_tokens[index] = get_token_object("OPERATOR", "RIGHTBLOCK")
                    index += 1
                    cmd = ""
                elif cmd == ";":
                    row_tokens[index] = get_token_object("OPERATOR", "APPOSTROF")
                    index += 1
                    cmd = ""

                elif cmd == "REM" and get_next(chars, c + 1) in self.INVISIBLE_CHAR_LIST:
                    # if it's a comment then it just skips it
                    row_tokens[index] = get_token_object("STATIC", "REM")
                    break
                elif cmd == "FALSE" and get_next(chars, c + 1) in self.INVISIBLE_CHAR_LIST:
                    row_tokens[index] = get_token_object("BOOLEAN", "FALSE")
                    index += 1
                    cmd = ""
                elif cmd == "TRUE" and get_next(chars, c + 1) in self.INVISIBLE_CHAR_LIST:
                    row_tokens[index] = get_token_object("BOOLEAN", "TRUE")
                    index += 1
                    cmd = ""

                elif cmd.isalpha() and cmd in self.KEYWORDS_LIST and get_next(chars, c + 1) in self.INVISIBLE_CHAR_LIST:
                    row_tokens[index] = get_token_object("STATIC", cmd)
                    index += 1
                    cmd = ""

                # check for var
                elif len(cmd) > 0 and get_next(chars, c + 1) in [" ", "\n", ",", "]"]:
                    row_tokens[index] = get_token_object("VAR", cmd)
                    index += 1
                    cmd = ""

                # check for variables a variable name can only be one char long
                # needs a lot of work
                elif len(cmd) > 0 and (get_next(chars, c + 1) == "["):
                    row_tokens[index] = get_token_object("VARARRAY", cmd)
                    index += 1
                    cmd = ""

            tokens[key] = row_tokens

        print(tokens)
        return tokens

    def get_command_map(self):
        return self.CommandMap
