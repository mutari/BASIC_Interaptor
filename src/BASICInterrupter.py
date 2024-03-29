from functionSet import FunctionSet
import traceback

from helpFunctions import token_row_slice


def get_index_of(data, val, index="value"):
    i = 0
    while i < len(data):
        if data[list(data.items())[i][0]][index] == val:
            return i
        i += 1
    return None


def find_row_index_by_key(tokens, key):
    tokens = list(tokens.keys())
    i = 0
    while i < len(tokens):
        if tokens[i] == str(key):
            return i
        i += 1
    return None


class Interrupter:
    STATIC = "STATIC"
    VAR_ARRAY = "VAR_ARRAY"
    VAR = "VAR"

    def __init__(self, set_manager, function_set_name, mode, new=True):
        self.rowIndex = 0
        self.new = new
        self.mode = mode
        if new:
            self.functions = FunctionSet(function_set_name, mode)
            self.manager = set_manager
            self.manager.add_set(self.functions)
        else:
            self.manager = set_manager
            self.functions = self.manager.get_by_name(function_set_name)

    def move_code_index(self, tokens, index=0):
        temp = list(tokens.keys())[index]
        self.rowIndex = index + 1
        return temp

    def new_interrupter(self, tokens, code):
        """
        Method: new_interrupter

        Description:
        This method creates a new Interrupter object and triggers the interrupt
        for a specific row in the code. It returns the row number if the interrupt
        is successful, otherwise it returns None.

        Parameters:
        - self: The instance of the current object.
        - tokens: A dictionary representing the line of tokens.
        - code: The code associated with the row to be interrupted.

        Returns:
        - If the interrupt has a goTo/goSub function it returns the new row number else it returns None
        """
        row = {}
        row_key = list(tokens.keys())[self.rowIndex - 1]
        row[row_key] = code
        # create a new interceptor white the same functionsSet
        number = Interrupter(self.manager, self.functions.name, self.mode, False).interrupt(row)
        if number:
            return self.move_code_index(tokens, find_row_index_by_key(tokens, number))
        return None

    def interrupt(self, tokens):

        code_index = self.move_code_index(tokens, self.rowIndex)

        while True:

            # code index is the row number
            # c is the index of the specific token in the row
            if len(list(tokens[code_index].items())) <= 0:
                print("Syntax error row: " + str(code_index))
                exit(1)
            c = list(tokens[code_index].items())[0][0]
            checking = tokens[code_index][c]

            try:

                if checking["type"] == Interrupter.STATIC:
                    # check is the command starts white a static key name
                    if checking["value"] == "REM":
                        if self.rowIndex < len(tokens):
                            code_index = self.move_code_index(tokens, self.rowIndex)
                        else:
                            break
                        continue
                    if checking["value"] == "PRINT":
                        self.functions.PRINT(token_row_slice(tokens[code_index], 1))
                    elif checking["value"] == "LET":
                        var_name = tokens[code_index][c + 1]
                        if tokens[code_index][c + 2]["value"] == "EQ":
                            self.functions.LET(var_name, token_row_slice(tokens[code_index], 3))
                        else:
                            print("Let error: " + str(checking) + " row(" + code_index + ")")
                            exit(1)
                    elif checking["value"] == "ARRAY":
                        array_name = tokens[code_index][c + 1]
                        array_dimension = 1
                        if c + 2 < len(tokens[code_index]) and tokens[code_index][c + 2]["value"] == "COMMA":
                            array_dimension = tokens[code_index][c + 3]["value"]
                        self.functions.ARRAY_CREATE(array_name, array_dimension)
                    elif checking["value"] == "INPUT":
                        data = token_row_slice(tokens[code_index], 1)
                        index = get_index_of(data, "APPOSTROF")
                        text = token_row_slice(data, 0, index)
                        var_name = data[list(token_row_slice(data, index + 1).items())[0][0]]
                        self.functions.INPUT(var_name, text)
                    elif checking["value"] == "END":
                        print("The Script Whs Terminated(row: " + code_index + ")")
                        exit(0)
                    elif checking["value"] == "GOTO":
                        number = self.functions.GOTO(token_row_slice(tokens[code_index], 1))
                        if not self.new:
                            return number
                        code_index = self.move_code_index(tokens, find_row_index_by_key(tokens, number))
                        continue
                    elif checking["value"] == "GOSUB":
                        number = self.functions.GOSUB(token_row_slice(tokens[code_index], 1), code_index)
                        if not self.new:
                            return number
                        code_index = self.move_code_index(tokens, find_row_index_by_key(tokens, number))
                        continue
                    elif checking["value"] == "NAMESPACE":
                        self.functions.NAMESPACE(token_row_slice(tokens[code_index], 1))
                    elif checking["value"] == "LOAD":
                        self.functions.LOAD(token_row_slice(tokens[code_index], 1))
                    elif checking["value"] == "IMPORT":
                        path = token_row_slice(tokens[code_index], 1, get_index_of(tokens[code_index], "AS"))
                        import_var = token_row_slice(tokens[code_index], get_index_of(tokens[code_index], "AS") + 1)
                        self.functions.IMPORT(path, import_var)
                        continue
                    elif checking["value"] == "RETURN":
                        number = self.functions.RETURN()
                        if number is not None:
                            code_index = self.move_code_index(tokens, find_row_index_by_key(tokens, number))
                            code_index = self.move_code_index(tokens, self.rowIndex)
                            continue
                    elif checking["value"] == "PAUSE":
                        self.functions.PAUSE(token_row_slice(tokens[code_index], 1))
                    elif checking["value"] == "IF":
                        statement = token_row_slice(tokens[code_index], 1, get_index_of(tokens[code_index], "THEN"))
                        code = token_row_slice(tokens[code_index], get_index_of(tokens[code_index], "THEN") + 1,
                                               get_index_of(tokens[code_index], "ELSE"))

                        if self.functions.IF(statement):
                            new_code_index = self.new_interrupter(tokens, code)
                            if new_code_index is not None:
                                code_index = new_code_index
                                continue
                        elif get_index_of(tokens[code_index], "ELSE") is not None:
                            alternative_code = token_row_slice(tokens[code_index],
                                                               get_index_of(tokens[code_index], "ELSE") + 1)
                            new_code_index = self.new_interrupter(tokens, alternative_code)
                            if new_code_index is not None:
                                code_index = new_code_index
                                continue

                    elif checking["value"] == "EXPORT":
                        self.functions.EXPORT(token_row_slice(tokens[code_index], 1))
                    elif checking["value"] == "FOR":
                        self.functions.FOR(token_row_slice(tokens[code_index], 1), code_index)
                    elif checking["value"] == "NEXT":
                        number = self.functions.NEXT(token_row_slice(tokens[code_index], 1))
                        if number is not None:
                            code_index = self.move_code_index(tokens, find_row_index_by_key(tokens, number))
                            code_index = self.move_code_index(tokens, self.rowIndex)
                            continue
                    else:
                        print("Undefined token: " + str(checking) + " row(" + code_index + ")")
                        exit(1)
                elif checking["type"] == Interrupter.VAR_ARRAY:
                    array_name = checking["value"]
                    # print(tokens[code_index])
                    keys = token_row_slice(tokens[code_index], 1)
                    # print("keys: " + str(keys))
                    self.functions.ARRAY_UPPDATE(array_name, keys)
                elif checking["type"] == Interrupter.VAR:
                    if tokens[code_index][c + 1]["value"] == "EQ":
                        # print(self.token_row_slice(tokens[code_index], 3))
                        self.functions.LET(checking, token_row_slice(tokens[code_index], 2))
                    else:
                        print("Error type: " + str(checking) + " row(" + code_index + ")")
                        exit(1)

                # move tokens list forward
                if self.rowIndex < len(tokens):
                    code_index = self.move_code_index(tokens, self.rowIndex)
                else:
                    break

            except Exception as e:
                if self.mode == 'dev':
                    print("An exception occurred: ", str(traceback.print_exc()))
                else:
                    print(f"""Error: {str(checking)} row({code_index})""")
                break
