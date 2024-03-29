import time
from helpFunctions import get_file_input, token_row_slice


def eval_num(input):
    out = ""
    for c in input:
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
            elif value == "SLASH":
                out += "/"
            elif value == "LEFTPARENTHESIS":
                out += "("
            elif value == "RIGHTPARENTHESIS":
                out += ")"
        else:
            return False

    return eval(out)


def is_number(char):
    return str(char).isdecimal()


def basic_print(value):
    print(value)


def basic_input(text):
    return input(text)


def get_key_of(data, val, index="value"):
    i = 0
    while i < len(data):
        if data[list(data.items())[i][0]][index] == val:
            return i
        i += 1
    return None


def eval_string(input):
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
        elif token["value"] != "PLUS" and token["value"] != "MINUS":
            return "Error evalStr input :: " + str(input)
        i += 1

    return out


class FunctionSet:

    def __init__(self, thread_name, mode):
        self.name = thread_name
        self.VarList = []
        self.ArrayList = []
        self.OldIndexes = []
        self.forLoop = []
        self.namespace = ""
        self.mode = mode

    # basic static functions
    def PRINT(self, tokens):
        output = self.advanced_eval(tokens)
        basic_print(output)

    def LET(self, name, value):
        self.create_new_var(name["value"], self.advanced_eval(value))

    def ARRAY_CREATE(self, name, dim):
        self.create_new_array(name["value"], dim)

    def ARRAY_UPPDATE(self, name, data):
        array = self.get_array_by_name(name)
        key = self.generate_array_keys(data)

        # test if the right amount of array keys
        if key["keysFound"] > int(array["dimension"]):
            print("to meny keys" + str(key) + " array: " + str(array))
            exit(1)
        elif key["keysFound"] < int(array["dimension"]):
            print("to fjue keys: " + str(key) + " array: " + str(array))
            exit(1)

        if data[list(data.items())[key["endOfKeys"]][0]]["value"] == "EQ":
            data = token_row_slice(data, key["endOfKeys"] + 1)
            value = self.advanced_eval(data)
            self.update_array(name, key["keys"], value)

    def INPUT(self, var_name, text):
        text = self.advanced_eval(text)
        value = basic_input(text)
        self.create_new_var(var_name["value"], value)

    def GOTO(self, data):
        number = self.advanced_eval(data)
        return number

    def GOSUB(self, data, old_index):
        number = self.advanced_eval(data)
        self.OldIndexes.append(old_index)
        return number

    def RETURN(self):
        try:
            return self.OldIndexes.pop(len(self.OldIndexes) - 1)
        except:
            return None

    def PAUSE(self, data):
        t = self.advanced_eval(data)
        time.sleep(t)

    def IF(self, case):
        operation_index = list(case.items())[get_key_of(case, "BOOLEANSKOP", "type")][0]
        operator = case[operation_index]["value"]
        value1 = self.advanced_eval(token_row_slice(case, 0, operation_index - 1))
        value2 = self.advanced_eval(token_row_slice(case, operation_index))
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

        if not is_number(value1):
            value1 = "\"" + str(value1) + "\""
        else:
            value1 = str(value1)

        if not is_number(value2):
            value2 = "\"" + str(value2) + "\""
        else:
            value2 = str(value2)

        return eval(value1 + " " + str(operator) + " " + value2)

    def FOR(self, data, row_index):
        key_to = get_key_of(data, "TO")
        key_step = get_key_of(data, "STEP")

        # create a variable
        var = token_row_slice(data, 0, key_to)
        var_name = var[1]
        if var[2]["value"] == "EQ":
            self.LET(var_name, token_row_slice(var, 2))
        else:
            print("Error interaptor: missing EQ when declaring var")
            exit(1)

        if key_step:
            goal = token_row_slice(data, key_to, key_step)
            step = token_row_slice(data, key_step + 1)
            step = self.advanced_eval(step)
        else:
            goal = token_row_slice(data, key_to + 1)
            step = 1
        goal = self.advanced_eval(goal)

        self.forLoop.append({"var": var_name, "goal": goal, "step": step, "row": row_index})

    def NEXT(self, var_name):
        loop = self.forLoop[len(self.forLoop) - 1]
        if loop["var"]["value"] != var_name[1]["value"]:
            print("For loops in wrong queue")
            exit(1)
        value = self.get_var_by_name(loop["var"]["value"])
        if int(value["value"]) + int(loop['step']) >= int(loop["goal"]):
            self.forLoop.pop(len(self.forLoop) - 1)
            self.uppdate_var(loop["var"]["value"], "None")  # borde ändra till att döda variablen
            return None
        self.uppdate_var(loop["var"]["value"], int(value["value"]) + int(loop["step"]))
        return loop["row"]

    def LOAD(self, data):
        name = list(data.items())[0][1]['value']
        if name == "NOW":
            self.create_new_var(name, int(time.time() * 1000000))
        elif name == "SEC":
            self.create_new_var(name, int(time.time()))

    def NAMESPACE(self, tokens):
        namespace = self.advanced_eval(tokens)
        self.namespace = namespace

    def IMPORT(self, path, import_var):

        command_list = get_file_input(path)
        print(command_list)

        print(path, import_var)

    def EXPORT(self, data):
        var = self.get_var_by_name(data[1]["value"])
        print("exp:" + str(var["name"]) + ":" + str(var["value"]))

    # var functions
    def get_var_by_name(self, name):
        name = self.get_namespace(name);
        for var in self.VarList:
            if var["name"] == name:
                return var
        print("Error: array whit name: " + str(name) + " is not deklarerad ")
        exit(1)

    def create_new_var(self, name, value):
        name = self.get_namespace(name);
        for var in self.VarList:
            if var["name"] == name:
                var["value"] = value  # if var exists overide it
                return
        self.VarList.append({"name": name, "value": value})
        # print(self.VarList)

    def uppdate_var(self, name, value):
        name = self.get_namespace(name);
        var = self.get_var_by_name(name)
        var["value"] = value

    # array functions
    def get_array_by_name(self, name):
        name = self.get_namespace(name);
        for array in self.ArrayList:
            if array["name"] == name:
                return array
        print("Error: array whit name: " + str(name) + " is not deklarerad ")
        exit(1)

    def create_new_array(self, name, dim):
        name = self.get_namespace(name)
        self.ArrayList.append({"name": name, "dimension": dim, "value_list": {}})

    def update_array(self, name, keys, value):
        array = self.get_array_by_name(name)
        array["value_list"][keys] = value

    def get_namespace(self, name):
        if len(name.split('@')) > 1:
            return name
        if self.namespace != "":
            name = self.namespace + "@" + name
        return name

    def generate_array_keys(self, data):
        keys = ""
        # get the arraý keys
        end_of_keys = -1
        keys_found = 0
        exp = False
        exp_obj = {}
        it = iter(range(list(data.items())[0][0], len(data) + list(data.items())[0][0]))
        for c in it:
            if data[c]["value"] == "LEFTBLOCK":
                exp = True
                continue
            elif data[c]["value"] == "RIGHTBLOCK":
                keys_found += 1
                if keys != "":
                    keys += ',' + str(self.advanced_eval(exp_obj))
                else:
                    keys += str(self.advanced_eval(exp_obj))
                exp_obj = {}
                exp = False
                if c + 1 >= len(data) + list(data.items())[0][0]:
                    end_of_keys = c - (int(list(data.items())[0][0]) - 1)
                    break
                elif data[c + 1]["value"] != "LEFTBLOCK":
                    end_of_keys = c - (int(list(data.items())[0][0]) - 1)
                    break
                else:
                    continue
            elif exp:
                exp_obj[c] = data[c]
            else:
                print("Array syntax error data :: " + str(data))
                exit()
        return {"endOfKeys": end_of_keys, "keysFound": keys_found, "keys": keys}

    # bas functions
    def get_name(self):
        return self.name

    # omvandlar variablar till des värde
    def translate(self, input):
        out = {}
        it = iter(range(0, len(input)))
        for c in it:
            # list(input.items())[0][0] gets the first key of the dic
            token = input[c + list(input.items())[0][0]]
            if token["type"] == "VAR":
                value = self.get_var_by_name(token["value"])["value"]
                if is_number(value):
                    out[c] = ({"type": "NUM", "value": value})
                else:
                    out[c] = ({"type": "STR", "value": value})
            elif token["type"] == "VAR_ARRAY":
                key = self.generate_array_keys(token_row_slice(input, c + 1))
                for j in range(0, key["endOfKeys"]):
                    next(it)
                value = self.get_array_by_name(token["value"])["value_list"][key["keys"]]
                if is_number(value):
                    out[c] = ({"type": "NUM", "value": value})
                else:
                    out[c] = ({"type": "STR", "value": value})
            else:
                out[c] = token
        return out

    def advanced_eval(self, value):
        # translates all the variabels to ther value
        trans = self.translate(value)

        # returns False if the value have a char that is not a number
        res = eval_num(trans)
        if res is False:
            # if value is not a string
            res = eval_string(trans)
        return res
